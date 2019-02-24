from behave import given, then, when
from behave import use_fixture
from django.core import mail
from features.fixtures import graphql_query
from saleor.account.models import User
from tests.api.utils import get_graphql_content

import features.types
import re


@when(u'un client inconnu fait une demande d\'enregistrement')
def step_impl(context):
    use_fixture(graphql_query, context, 'signin.graphql')
    variables = {
        'email': context.unknown['email'],
        'password': context.unknown['password']
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
    context.test.assertEqual(User.objects.filter(email=context.unknown['email']).count(), 1)


@then(u'il est inactif')
def step_impl(context):
    user = User.objects.filter(email=context.unknown['email'])
    context.test.assertFalse(user.is_active)
