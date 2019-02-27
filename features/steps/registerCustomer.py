from behave import given, then, when
from behave import use_fixture
from django.core import mail
from features.fixtures import graphql_query
from saleor.account.models import User
from shopozor.models import HackerAbuseEvents
from tests.api.utils import get_graphql_content

import re

# TODO: this must be stored somewhere else in a lib
account_activation_pattern = r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'


def sign_user_in(context, email):
    use_fixture(graphql_query, context, 'signin.graphql')
    variables = {
        'email': context.unknown['email']
    }
    response = context.test.client.post_graphql(context.query, variables)
    return get_graphql_content(response)


def get_credentials_from_confirmation_email(mail_body):
    match = re.search(account_activation_pattern, mail_body)
    return {
        'uidb64': match.group('uidb64'),
        'token': match.group('token')
    }


@given(u'un client qui a reçu un lien de confirmation de création de compte')
def step_impl(context):
    context.response = sign_user_in(context, context.unknown['email'])
    mail_body = mail.outbox[0].body
    context.credentials = get_credentials_from_confirmation_email(mail_body)


@when(u'un client inconnu fait une demande d\'enregistrement')
def step_impl(context):
    context.response = sign_user_in(context, context.unknown['email'])


@when(u'un utilisateur fait une demande d\'enregistrement avec un e-mail déjà connu')
def step_impl(context):
    sign_user_in(context, context.consumer['email'])


def activate_account(context, uidb64, token, password):
    use_fixture(graphql_query, context, 'activateCustomer.graphql')
    variables = {
        'encodedUserId': uidb64,
        'oneTimeToken': token,
        'password': password
    }
    response = context.test.client.post_graphql(context.query, variables)
    context.response = get_graphql_content(response)


@when(u'il définit son mot de passe dans les temps')
def step_impl(context):
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    password = context.unknown['password']
    activate_account(context, uidb64, token, password)


@then(u'il reçoit un e-mail avec un lien de confirmation de création de compte')
def step_impl(context):
    context.test.assertEqual(len(mail.outbox), 1)
    mail_body = mail.outbox[0].body
    match = re.search(account_activation_pattern, mail_body)
    context.test.assertIsNotNone(match)


@then(u'son compte est créé')
def step_impl(context):
    context.test.assertEqual(len(context.response['data']['signin']['errors']), 0)
    context.test.assertEqual(User.objects.filter(email=context.unknown['email']).count(), 1)


@then(u'il est inactif')
def step_impl(context):
    user = User.objects.filter(email=context.unknown['email'])
    context.test.assertFalse(user.is_active)


@then(u'il n\'obtient aucun message d\'erreur')
def step_impl(context):
    context.test.assertEqual(context.response['data'], context.successful_signin['data'])


@then(u'un message d\'avertissement est envoyé à cet e-mail')
def step_impl(context):
    context.test.assertEqual(len(mail.outbox), 1)
    email = mail.outbox[0]
    context.test.assertTrue(context.consumer['email'] in email.recipients())


@then(u'le Shopozor enregistre l\'incident dans son journal')
def step_impl(context):
    entry = HackerAbuseEvents.objects.latest('timestamp')
    context.test.assertEqual(entry.user.email, context.consumer['email'])


@then(u'son compte est activé')
def step_impl(context):
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


@then(u'son lien de confirmation est invalidé')
def step_impl(context):
    uidb64 = context.credentials['uidb64']
    token = context.credentials['token']
    password = context.unknown['password']
    activate_account(context, uidb64, token, password)
    context.test.assertEqual(context.response['data'], context.expired_account_confirmation_link['data'])
