from behave import given, then, when
from behave import use_fixture
from datetime import datetime
from datetime import timedelta
from django.core import mail
from features.fixtures import graphql_query
from freezegun import freeze_time
from saleor.account.models import User
from shopozor.models import HackerAbuseEvents
from tests.api.utils import get_graphql_content

import re

# TODO: this must be stored somewhere else in a lib:
# the pattern needs to be used here to extract the uid and the token
# it will be needed in the mutation's code to extract the same data
account_activation_pattern = r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'


def sign_user_up(context, email):
    use_fixture(graphql_query, context, 'signup.graphql')
    variables = {
        'email': email
    }
    response = context.test.client.post_graphql(context.query, variables)
    return get_graphql_content(response)


def get_credentials_from_confirmation_email(mail_body):
    match = re.search(account_activation_pattern, mail_body)
    return {
        'uidb64': match.group('uidb64'),
        'token': match.group('token')
    }


@given(u'un nouveau client qui a reçu un lien d\'activation de compte')
def step_impl(context):
    context.response = sign_user_up(context, context.unknown['email'])
    mail_body = mail.outbox[0].body
    context.credentials = get_credentials_from_confirmation_email(mail_body)
    context.email_reception_time = datetime.now()


def activate_account(context, uidb64, token, password):
    use_fixture(graphql_query, context, 'activateCustomer.graphql')
    variables = {
        'encodedUserId': uidb64,
        'oneTimeToken': token,
        'password': password
    }
    response = context.test.client.post_graphql(context.query, variables)
    context.response = get_graphql_content(response)


@given(u'qui a déjà activé son compte')
def step_impl(context):
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    password = context.unknown['password']
    activate_account(context, uidb64, token, password)
    context.test.assertEqual(context.response['data'], context.successful_account_confirmation['data'])


@when(u'un client inconnu fait une demande d\'enregistrement')
def step_impl(context):
    context.response = sign_user_up(context, context.unknown['email'])


@when(u'un utilisateur fait une demande d\'enregistrement avec l\'e-mail d\'un compte inactif')
def step_impl(context):
    context.response = sign_user_up(context, context.inactive_customer['email'])


@when(u'un utilisateur fait une demande d\'enregistrement avec l\'e-mail d\'un compte actif')
def step_impl(context):
    sign_user_up(context, context.consumer['email'])


@when(u'il active son compte avec un mot de passe conforme au plus tard {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    elapsed_time_since_email_reception_in_seconds = (datetime.now() - context.email_reception_time).total_seconds()
    context.test.assertTrue(elapsed_time_since_email_reception_in_seconds < expiration_delta_in_seconds)
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    password = context.unknown['password']
    activate_account(context, uidb64, token, password)


@when(u'il active son compte avec un mot de passe non conforme au plus tard {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    elapsed_time_since_email_reception_in_seconds = (datetime.now() - context.email_reception_time).total_seconds()
    context.test.assertTrue(elapsed_time_since_email_reception_in_seconds < expiration_delta_in_seconds)
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    password = 'abdc'
    activate_account(context, uidb64, token, password)


@when(u'il active son compte avec un mot de passe conforme {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    datetime_after_expiration = context.email_reception_time + timedelta(seconds=expiration_delta_in_seconds)
    with freeze_time(datetime_after_expiration):
        uidb64 = context.credentials['uidb64']
        token = context.credentials['token']
        password = context.unknown['password']
        activate_account(context, uidb64, token, password)


@when(u'il l\'active pour la deuxième fois')
def step_impl(context):
    user = User.objects.filter(email=context.unknown['email'])
    context.current_encrypted_password = user.password
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    password = context.unknown['password'] + 'a'
    activate_account(context, uidb64, token, password)


@then(u'il reçoit un e-mail avec un lien d\'activation de compte')
def step_impl(context):
    context.test.assertEqual(len(mail.outbox), 1)
    mail_body = mail.outbox[0].body
    match = re.search(account_activation_pattern, mail_body)
    context.test.assertIsNotNone(match)


@then(u'son compte est créé')
def step_impl(context):
    context.test.assertEqual(len(context.response['data']['customerCreate']['errors']), 0)
    context.test.assertEqual(User.objects.filter(email=context.unknown['email']).count(), 1)


def assert_account_is_inactive(email, context):
    user = User.objects.filter(email=email)
    context.test.assertFalse(user.is_active)


@then(u'son compte reste inactif')
def step_impl(context):
    assert_account_is_inactive(context.unknown['email'], context)


@then(u'il est inactif')
def step_impl(context):
    assert_account_is_inactive(context.unknown['email'], context)


@then(u'il n\'obtient aucun message d\'erreur')
def step_impl(context):
    context.test.assertEqual(context.response['data'], context.successful_signup['data'])


@then(u'un message d\'avertissement est envoyé à cet e-mail')
def step_impl(context):
    context.test.assertEqual(len(mail.outbox), 1)
    email = mail.outbox[0]
    context.test.assertTrue(context.consumer['email'] in email.recipients())


@then(u'l\'incident est enregistré dans un journal')
def step_impl(context):
    entry = HackerAbuseEvents.objects.latest('timestamp')
    context.test.assertEqual(entry.user.email, context.consumer['email'])


@then(u'son compte est activé')
def step_impl(context):
    context.test.assertEqual(context.response['data'], context.successful_account_confirmation['data'])
    user = User.objects.filter(email=context.unknown['email'])
    context.test.assertTrue(user.is_active)


@then(u'son mot de passe est sauvegardé')
def step_impl(context):
    user = User.objects.filter(email=context.unknown['email'])
    context.test.assertTrue(user.password)


@then(u'il n\'est pas identifié')
def step_impl(context):
    user = User.objects.filter(email=context.unknown['email'])
    context.test.assertFalse(user.token)
    context.test.assertFalse('token' in context.response['data']['customerActivate'])


@then(u'son lien d\'activation est invalidé')
def step_impl(context):
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    password = context.unknown['password']
    activate_account(context, uidb64, token, password)
    context.test.assertEqual(context.response['data'], context.expired_account_confirmation_link['data'])


@then(u'il obtient un message d\'erreur stipulant que le lien a expiré')
def step_impl(context):
    context.test.assertEqual(context.response['data'], context.expired_account_confirmation_link['data'])


@then(u'son compte est supprimé')
def step_impl(context):
    context.test.assertEqual(User.objects.filter(email=context.unknown['email']).count(), 0)


@then(u'son mot de passe reste inchangé')
def step_impl(context):
    user = User.objects.filter(email=context.unknown['email'])
    context.test.assertEqual(user.password, context.current_encrypted_password)
