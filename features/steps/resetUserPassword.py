from behave import given, then, when
from datetime import datetime, timedelta
from django.core import mail
from features.utils.auth.account_handling import get_current_encrypted_password
from features.utils.auth.credentials_checks import assertPasswordIsCompliant, assertPasswordIsNotCompliant
from features.utils.auth.mail_confirmation import ActivationMailHandler, gather_email_activation_data, check_that_email_was_sent_to_user
from features.utils.auth.password_generation import RandomCompliantPasswordGenerator
from features.utils.graphql.loader import get_query_from_file
from freezegun import freeze_time
from saleor.account.models import User
from tests.api.utils import get_graphql_content

import features.types

activation_url_prefix = 'reset'


def reset_password(client, user_email):
    raise NotImplementedError('reset_password method not implemented yet')


def set_new_compliant_password(context, uidb64, token):
    password_generator = RandomCompliantPasswordGenerator()
    compliant_password = password_generator.get_compliant_password()
    assertPasswordIsCompliant(compliant_password)
    context.new_password = compliant_password
    # TODO: set the new password with graphql!
    raise NotImplementedError(
        'set_new_compliant_password method not implemented yet')


def set_new_non_compliant_password(test, uidb64, token):
    non_compliant_password = 'non compliant password'
    assertPasswordIsNotCompliant(test, non_compliant_password)
    # TODO: set the new password with graphql!
    raise NotImplementedError(
        'set_new_non_compliant_password method not implemented yet')


def registered_user(context, persona):
    switch = {
        'Consommateur': context.consumer,
        'Producteur': context.producer,
        'Responsable': context.manager,
        'Rex': context.rex,
        'Softozor': context.softozor,
    }
    user = switch[persona]
    user['encrypted_password'] = get_current_encrypted_password(user['email'])
    return user


@given(u'un {persona:PersonaType} qui a reçu un lien de réinitialisation de mot de passe')
def step_impl(context, persona):
    context.current_user = registered_user(context, persona)
    test_client = context.test.test_client
    context.response = reset_password(
        test_client, context.current_user['email'])
    check_that_email_was_sent_to_user(
        context.test, context.current_user['email'])
    context.credentials = gather_email_activation_data(activation_url_prefix)
    context.test.assertIsNotNone(context.credentials)
    context.email_reception_time = datetime.now()


@given(u'qui a déjà réinitialisé son mot de passe avec ce lien')
def step_impl(context):
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    context.response = set_new_compliant_password(context, uidb64, token)
    # TODO: double-check that the response really corresponds to the desired graphql query
    context.test.assertEqual(
        context.response['data'], context.successful_set_password['data'])
    context.current_user['encrypted_password'] = get_current_encrypted_password(
        context.current_user['email'])


@when(u'un {persona:PersonaType} enregistré fait une demande de réinitialisation de mot de passe')
def step_impl(context, persona):
    context.current_user = registered_user(context, persona)
    test_client = context.test.test_client
    context.response = reset_password(
        test_client, context.current_user['email'])


@when(u'un utilisateur inconnu fait une demande de réinitialisation de mot de passe')
def step_impl(context):
    context.current_user = context.unknown
    test_client = context.test.test_client
    context.response = reset_password(
        test_client, context.current_user['email'])


@when(u'il définit un mot de passe conforme au plus tard {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    elapsed_time_since_email_reception_in_seconds = (
        datetime.now() - context.email_reception_time).total_seconds()
    context.test.assertTrue(
        elapsed_time_since_email_reception_in_seconds < expiration_delta_in_seconds)
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    context.response = set_new_compliant_password(context, uidb64, token)


@when(u'il définit un mot de passe non conforme au plus tard {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    elapsed_time_since_email_reception_in_seconds = (
        datetime.now() - context.email_reception_time).total_seconds()
    context.test.assertTrue(
        elapsed_time_since_email_reception_in_seconds < expiration_delta_in_seconds)
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    context.response = set_new_non_compliant_password(
        context.test, uidb64, token)


@when(u'il le réinitialise pour la deuxième fois avant l\'expiration du lien')
def step_impl(context):
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    context.response = set_new_compliant_password(context, uidb64, token)


@when(u'il définit un mot de passe conforme {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    datetime_after_expiration = context.email_reception_time + \
        timedelta(seconds=expiration_delta_in_seconds)
    with freeze_time(datetime_after_expiration):
        uidb64 = context.credentials['uidb64']
        token = context.credentials['token']
        context.response = set_new_compliant_password(context, uidb64, token)


@then(u'il reçoit un e-mail de réinitialisation de mot de passe')
def step_impl(context):
    check_that_email_was_sent_to_user(
        context.test, context.current_user['email'])
    credentials = gather_email_activation_data(activation_url_prefix)
    context.test.assertIsNotNone(credentials)


@then(u'son mot de passe reste inchangé')
def step_impl(context):
    user = User.objects.filter(email=context.current_user['email'])
    context.test.assertEqual(
        context.current_user['encrypted_password'], user.password)


@then(u'il ne reçoit pas d\'e-mail de réinitialisation de compte')
def step_impl(context):
    context.test.assertEqual(0, len(mail.outbox))


@then(u'son nouveau mot de passe est sauvegardé')
def step_impl(context):
    context.test.assertEqual(context.successful_set_password, context.response)
    # Additionally, we check that the new password can be used:
    query = get_query_from_file('login.graphql')
    variables = {
        'email': context.current_user['email'],
        'password': context.new_password
    }
    response = context.test.client.post_graphql(query, variables)
    content = get_graphql_content(response)
    login_data = content['data']['login']
    context.test.assertIsNotNone(login_data['token'])
    context.test.assertEqual(0, len(login_data['errors']))


@then(u'son lien de réinitialisation est invalidé')
def step_impl(context):
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    response = set_new_compliant_password(context, uidb64, token)
    # TODO: verify that this fixture corresponds to the desired graphql query!
    context.test.assertEqual(
        context.expired_password_reset_link['data'], response['data'])
