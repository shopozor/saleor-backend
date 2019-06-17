from behave import given, then, when
from datetime import datetime, timedelta
from django.core import mail
from features.utils.auth.account_handling import get_current_encrypted_password
from features.utils.auth.credentials_checks import assertPasswordIsCompliant, assertPasswordIsNotCompliant
from features.utils.auth.mail_confirmation import ActivationMailHandler, gather_email_activation_data, check_that_email_was_sent_to_user, check_that_email_is_received_soon_enough, check_compulsory_password_reinit_credential_arguments
from features.utils.auth.password_generation import RandomCompliantPasswordGenerator
from features.utils.graphql.loader import get_query_from_file
from freezegun import freeze_time
from saleor.account.models import User
from tests.api.utils import get_graphql_content

import features.types

activation_url_prefix = 'reset'


def reset_password(client, user_email):
    query = get_query_from_file('passwordReset.graphql')
    variables = {
        'email': user_email
    }
    response = client.post_graphql(query, variables)
    return get_graphql_content(response)


def set_new_password(client, **kwargs):
    check_compulsory_password_reinit_credential_arguments(kwargs)
    query = get_query_from_file('setPassword.graphql')
    response = client.post_graphql(query, kwargs)
    return get_graphql_content(response)


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
    password_generator = RandomCompliantPasswordGenerator()
    context.credentials['password'] = password_generator.get_compliant_password()
    assertPasswordIsCompliant(context.credentials['password'])
    test_client = context.test.test_client
    response = set_new_password(test_client, **context.credentials)
    context.test.assertEqual(
        response, context.successful_set_password)
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
    check_that_email_is_received_soon_enough(
        context, expiration_delta_in_seconds)
    password_generator = RandomCompliantPasswordGenerator()
    context.credentials['password'] = password_generator.get_compliant_password()
    assertPasswordIsCompliant(context.credentials['password'])
    test_client = context.test.test_client
    context.response = set_new_password(test_client, **context.credentials)


@when(u'il définit un mot de passe non conforme au plus tard {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    check_that_email_is_received_soon_enough(
        context, expiration_delta_in_seconds)
    context.credentials['password'] = 'non-compliant-password'
    assertPasswordIsNotCompliant(context.test, context.credentials['password'])
    test_client = context.test.test_client
    context.response = set_new_password(test_client, **context.credentials)


@when(u'il le réinitialise pour la deuxième fois avant l\'expiration du lien')
def step_impl(context):
    password_generator = RandomCompliantPasswordGenerator()
    context.credentials['password'] = password_generator.get_compliant_password()
    assertPasswordIsCompliant(context.credentials['password'])
    test_client = context.test.test_client
    context.response = set_new_password(test_client, **context.credentials)


@when(u'il définit un mot de passe conforme {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    datetime_after_expiration = context.email_reception_time + \
        timedelta(seconds=expiration_delta_in_seconds)
    with freeze_time(datetime_after_expiration):
        password_generator = RandomCompliantPasswordGenerator()
        context.credentials['password'] = password_generator.get_compliant_password(
        )
        assertPasswordIsCompliant(context.credentials['password'])
        test_client = context.test.test_client
        context.response = set_new_password(test_client, **context.credentials)


@then(u'il reçoit un e-mail de réinitialisation de mot de passe')
def step_impl(context):
    check_that_email_was_sent_to_user(
        context.test, context.current_user['email'])
    credentials = gather_email_activation_data(activation_url_prefix)
    context.test.assertIsNotNone(credentials)
    context.test.assertEqual(
        context.successful_password_reset, context.response)


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
    # TODO: use login method from logUserIn.py
    query = get_query_from_file('login.graphql')
    variables = {
        'email': context.current_user['email'],
        'password': context.credentials['password']
    }
    response = context.test.client.post_graphql(query, variables)
    content = get_graphql_content(response)
    login_data = content['data']['login']
    context.test.assertIsNotNone(login_data['token'])
    context.test.assertEqual(0, len(login_data['errors']))


@then(u'son lien de réinitialisation est invalidé')
def step_impl(context):
    password_generator = RandomCompliantPasswordGenerator()
    context.credentials['password'] = password_generator.get_compliant_password()
    assertPasswordIsCompliant(context.credentials['password'])
    test_client = context.test.test_client
    response = set_new_password(test_client, **context.credentials)
    context.test.assertEqual(
        context.expired_password_reset_link, response)
