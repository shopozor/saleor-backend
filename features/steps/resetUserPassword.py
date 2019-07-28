from behave import given, then, when
from copy import deepcopy
from datetime import datetime, timedelta
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from features.utils.auth.queries import login
from features.utils.auth.account_handling import get_current_encrypted_password
from features.utils.auth.credentials_checks import assertPasswordIsCompliant, assertPasswordIsNotCompliant
from features.utils.auth.mail_confirmation import ActivationMailHandler, gather_email_activation_data, check_that_email_was_sent_to_user, check_that_email_is_received_soon_enough, check_compulsory_password_reinit_credential_arguments
from features.utils.auth.password_generation import RandomCompliantPasswordGenerator
from features.utils.graphql.loader import get_query_from_file
from freezegun import freeze_time
from saleor.account.models import User
from test_utils.url_utils import url_reset
from tests.api.utils import get_graphql_content

import features.types


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
    user = deepcopy(switch[persona])
    user['encrypted_password'] = get_current_encrypted_password(user['email'])
    return user


@given(u'un {persona:PersonaType} qui a reçu un lien de réinitialisation de mot de passe')
def step_impl(context, persona):
    context.current_user = registered_user(context, persona)
    test_client = context.test.client
    context.response = reset_password(
        test_client, context.current_user['email'])
    check_that_email_was_sent_to_user(
        context.test, context.current_user['email'])
    context.credentials = gather_email_activation_data(url_reset())
    context.test.assertIsNotNone(context.credentials)
    context.email_reception_time = datetime.now()


@given(u'qui a déjà réinitialisé son mot de passe avec ce lien')
def step_impl(context):
    password_generator = RandomCompliantPasswordGenerator()
    context.credentials['password'] = password_generator.get_compliant_password()
    assertPasswordIsCompliant(context.credentials['password'])
    test_client = context.test.client
    response = set_new_password(test_client, **context.credentials)
    context.test.assertEqual(
        response, context.successful_set_password)
    context.current_user['encrypted_password'] = get_current_encrypted_password(
        context.current_user['email'])


@when(u'un {persona:PersonaType} enregistré fait une demande de réinitialisation de mot de passe')
def step_impl(context, persona):
    context.current_user = registered_user(context, persona)
    test_client = context.test.client
    context.response = reset_password(
        test_client, context.current_user['email'])


@when(u'un utilisateur inconnu fait une demande de réinitialisation de mot de passe')
def step_impl(context):
    context.current_user = deepcopy(context.unknown)
    test_client = context.test.client
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
    test_client = context.test.client
    context.response = set_new_password(test_client, **context.credentials)


@when(u'il définit un mot de passe non conforme au plus tard {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    check_that_email_is_received_soon_enough(
        context, expiration_delta_in_seconds)
    context.credentials['password'] = 'non-compliant-password'
    assertPasswordIsNotCompliant(context.test, context.credentials['password'])
    test_client = context.test.client
    context.response = set_new_password(test_client, **context.credentials)


@when(u'il le réinitialise pour la deuxième fois avant l\'expiration du lien')
def step_impl(context):
    password_generator = RandomCompliantPasswordGenerator()
    context.credentials['password'] = password_generator.get_compliant_password()
    assertPasswordIsCompliant(context.credentials['password'])
    test_client = context.test.client
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
        test_client = context.test.client
        context.response = set_new_password(test_client, **context.credentials)


@then(u'il reçoit un e-mail de réinitialisation de mot de passe')
def step_impl(context):
    check_that_email_was_sent_to_user(
        context.test, context.current_user['email'])
    credentials = gather_email_activation_data(url_reset())
    context.test.assertIsNotNone(credentials)
    context.test.assertEqual(
        context.successful_password_reset, context.response)


@then(u'son mot de passe reste inchangé')
def step_impl(context):
    user = User.objects.filter(email=context.current_user['email']).get()
    context.test.assertEqual(
        context.current_user['encrypted_password'], user.password)


@then(u'il ne reçoit pas d\'e-mail de réinitialisation de compte')
def step_impl(context):
    context.test.assertEqual(0, len(mail.outbox))


@then(u'son nouveau mot de passe est sauvegardé')
def step_impl(context):
    context.test.assertEqual(context.successful_set_password, context.response)
    test_client = context.test.client
    content = login(
        test_client, email=context.current_user['email'], password=context.credentials['password'])
    login_data = content['data']['login']
    context.test.assertIsNotNone(login_data['token'])
    context.test.assertEqual(0, len(login_data['errors']))


@then(u'son lien de réinitialisation est invalidé')
def step_impl(context):
    password_generator = RandomCompliantPasswordGenerator()
    context.credentials['password'] = password_generator.get_compliant_password()
    assertPasswordIsCompliant(context.credentials['password'])
    test_client = context.test.client
    response = set_new_password(test_client, **context.credentials)
    context.test.assertEqual(
        context.expired_link, response['data']['setPassword'])


def get_user_instance_from_encoded_user_id(encoded_user_id):
    decoded_user_id = urlsafe_base64_decode(encoded_user_id).decode()
    return User.objects.get(pk=decoded_user_id)


@then(u'son lien de réinitialisation reste valide')
def step_impl(context):
    encoded_user_id = context.credentials['encodedUserId']
    decoded_user = get_user_instance_from_encoded_user_id(encoded_user_id)
    token = context.credentials['oneTimeToken']
    context.test.assertTrue(
        default_token_generator.check_token(decoded_user, token))


@then(u'il obtient un message d\'erreur stipulant que son mot de passe n\'est pas conforme')
def step_impl(context):
    context.test.assertEqual(context.password_not_compliant, context.response)
