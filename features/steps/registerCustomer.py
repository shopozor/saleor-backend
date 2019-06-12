from behave import given, then, when
from behave import use_fixture
from datetime import datetime
from datetime import timedelta
from django.core import mail
from features.fixtures import graphql_query
from features.utils.auth.mail_confirmation import ActivationMailHandler
from features.utils.auth.account_handling import get_current_encrypted_password, account_exists, is_active_account
from features.utils.graphql.loader import get_query_from_file
from features.utils.auth.credentials_checks import check_compulsory_credential_arguments
from freezegun import freeze_time
from shopozor.models import HackerAbuseEvents
from tests.api.utils import get_graphql_content

import re

activation_url_prefix = 'activate'


def signup(client, **kwargs):
    check_compulsory_credential_arguments(kwargs)

    query = get_query_from_file('signup.graphql')
    response = client.post_graphql(query, kwargs)
    return get_graphql_content(response)


def activate_account(client, uidb64, token):
    query = get_query_from_file('activateCustomer.graphql')
    variables = {
        'encodedUserId': uidb64,
        'oneTimeToken': token
    }
    response = client.post_graphql(query, variables)
    return get_graphql_content(response)


@given(u'un nouveau client qui a reçu un lien d\'activation de compte')
def step_impl(context):
    context.current_user = context.unknown
    test_client = context.test.client
    context.response = signup(test_client, **context.current_user)
    mail_handler = ActivationMailHandler(activation_url_prefix)
    mail_body = mail.outbox[0].body
    context.credentials = mail_handler.get_credentials(mail_body)
    context.email_reception_time = datetime.now()


@given(u'qui a déjà activé son compte')
def step_impl(context):
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    test_client = context.test.client
    context.response = activate_account(test_client, uidb64, token)
    context.test.assertEqual(
        context.response['data'], context.successful_account_confirmation['data'])


@when(u'un client inconnu fait une demande d\'enregistrement avec un mot de passe conforme')
def step_impl(context):
    context.current_user = context.unknown
    # TODO: assert password compliance
    test_client = context.test.client
    context.response = signup(test_client, **context.current_user)


@when(u'un utilisateur fait une demande d\'enregistrement avec l\'e-mail d\'un compte inactif et un mot de passe conforme')
def step_impl(context):
    context.current_user = context.inactive_customer
    # TODO: assert password compliance
    test_client = context.test.client
    context.response = signup(test_client, **context.current_user)


@when(u'un utilisateur fait une demande d\'enregistrement avec l\'e-mail d\'un compte inactif et un mot de passe non conforme')
def step_impl(context):
    context.current_user = context.inactive_customer
    context.current_encrypted_password = get_current_encrypted_password(
        context.current_user['email'])
    # an empty password is not compliant
    context.current_user['password'] = ''
    # TODO: assert password non-compliance
    test_client = context.test.client
    context.response = signup(test_client, **context.current_user)


@when(u'un utilisateur fait une demande d\'enregistrement avec l\'e-mail d\'un compte actif et un mot de passe conforme')
def step_impl(context):
    # in this case, the choice of the password is irrelevant; it must only comply to the password policy
    context.current_user = context.consumer
    # TODO: assert password compliance
    test_client = context.test.client
    context.response = signup(test_client, **context.current_user)


@when(u'il active son compte au plus tard {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    elapsed_time_since_email_reception_in_seconds = (
        datetime.now() - context.email_reception_time).total_seconds()
    context.test.assertTrue(
        elapsed_time_since_email_reception_in_seconds < expiration_delta_in_seconds)
    test_client = context.test.client
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    context.response = activate_account(test_client, uidb64, token)


@when(u'il active son compte {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    datetime_after_expiration = context.email_reception_time + \
        timedelta(seconds=expiration_delta_in_seconds)
    with freeze_time(datetime_after_expiration):
        test_client = context.test.client
        uidb64 = context.credentials['uidb64']
        token = context.credentials['token']
        context.response = activate_account(test_client, uidb64, token)


@when(u'il l\'active pour la deuxième fois avant l\'expiration du lien')
def step_impl(context):
    # we don't need to check that the link hasn't expired
    # because we are guaranteed to have waited a very little
    # amount of time here
    test_client = context.test.client
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    context.response = activate_account(test_client, uidb64, token)


@then(u'il reçoit un e-mail avec un lien d\'activation de compte')
def step_impl(context):
    context.test.assertEqual(len(mail.outbox), 1)
    mail_body = mail.outbox[0].body
    mail_handler = ActivationMailHandler(activation_url_prefix)
    credentials = mail_handler.get_credentials(mail_body)
    context.test.assertIsNotNone(credentials)


@then(u'il obtient un message d\'erreur stipulant que son mot de passe n\'est pas conforme à la politique des mots de passe')
def step_impl(context):
    context.test.assertEqual(
        context.response['data'], context.password_not_compliant_response['data'])


@then(u'son compte est créé')
def step_impl(context):
    context.test.assertEqual(
        len(context.response['data']['customerCreate']['errors']), 0)
    context.test.assertTrue(account_exists(context.current_user['email']))


@then(u'son compte n\'est pas créé')
def step_impl(context):
    context.test.assertFalse(account_exists(context.current_user['email']))


@then(u'son compte reste inactif')
def step_impl(context):
    context.test.assertFalse(is_active_account(context.current_user['email']))


@then(u'son compte est inactif')
def step_impl(context):
    context.test.assertFalse(is_active_account(context.current_user['email']))


@then(u'il ne reçoit pas d\'e-mail d\'activation de compte')
def step_impl(context):
    context.test.assertEqual(len(mail.outbox), 0)


@then(u'il n\'obtient aucun message d\'erreur')
def step_impl(context):
    context.test.assertEqual(
        context.response['data'], context.successful_signup['data'])


@then(u'un message d\'avertissement est envoyé à cet e-mail')
def step_impl(context):
    context.test.assertEqual(len(mail.outbox), 1)
    email = mail.outbox[0]
    context.test.assertTrue(
        context.current_user['email'] in email.recipients())


@then(u'l\'incident est enregistré dans un journal')
def step_impl(context):
    entry = HackerAbuseEvents.objects.latest('timestamp')
    context.test.assertEqual(entry.user.email, context.current_user['email'])


@then(u'son compte est activé')
def step_impl(context):
    context.test.assertEqual(
        context.response['data'], context.successful_account_confirmation['data'])
    context.test.assertTrue(is_active_account(context.current_user['email']))


@then(u'son mot de passe est sauvegardé')
def step_impl(context):
    user = User.objects.filter(email=context.unknown['email'])
    context.test.assertTrue(user.password)


@then(u'son mot de passe n\'est pas sauvegardé')
def step_impl(context):
    context.test.assertEqual(context.current_encrypted_password,
                             get_current_encrypted_password(context.current_user['email']))


@then(u'il n\'est pas identifié')
def step_impl(context):
    context.test.assertFalse(
        'token' in context.response['data']['customerActivate'])


@then(u'son lien d\'activation est invalidé')
def step_impl(context):
    test_client = context.test.client
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    context.response = activate_account(test_client, uidb64, token)
    context.test.assertEqual(
        context.response['data'], context.expired_account_confirmation_link['data'])


@then(u'il obtient un message d\'erreur stipulant que le lien a expiré')
def step_impl(context):
    context.test.assertEqual(
        context.response['data'], context.expired_account_confirmation_link['data'])
