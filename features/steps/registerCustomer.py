from behave import given, then, when
from behave import use_fixture
from django.core import mail
from features.fixtures import graphql_query
from saleor.account.models import User
from tests.api.utils import get_graphql_content

import re


@when(u'un client inconnu fait une demande d\'enregistrement')
def step_impl(context):
    use_fixture(graphql_query, context, 'signin.graphql')
    variables = {
        'email': context.unknown['email']
    }
    response = context.test.client.post_graphql(context.query, variables)
    context.response = get_graphql_content(response)


@when(u'un utilisateur fait une demande d\'enregistrement avec un e-mail déjà connu')
def step_impl(context):
    use_fixture(graphql_query, context, 'signin.graphql')
    variables = {
        'email': context.consumer['email']
    }
    response = context.test.client.post_graphql(context.query, variables)
    context.response = get_graphql_content(response)


@then(u'il reçoit un e-mail avec un lien de confirmation de création de compte')
def step_impl(context):
    context.test.assertEqual(len(mail.outbox), 1)
    mail_body = mail.outbox[0].body
    match = re.search(r'https?:\/\/www\.[a-z -]+\.ch\/activate\/.+\/.+', mail_body)
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
    context.test.assertEqual(len(context.response['data']['signin']['errors']), 0)


@then(u'un message d\'avertissement est envoyé à cet e-mail')
def step_impl(context):
    context.test.assertEqual(len(mail.outbox), 1)
    email = mail.outbox[0]
    context.test.assertTrue(context.consumer['email'] in email.recipients())


@then(u'le Shopozor enregistre l\'incident dans son journal')
def step_impl(context):
    # TODO: that table is something that should appear in Softozor's dashboard
    # we want: email, timestamp, message (something like "Possible account abuse"), potential hacker ip?
    entry = HackerAbuse.objects.latest('timestamp')
    context.test.assertEqual(entry.email, context.consumer['email'])
