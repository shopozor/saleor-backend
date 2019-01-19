from behave import given, then, when
from behave import use_fixture

from features.fixtures.graphql import graphql_query
from tests.api.utils import get_graphql_content

import features.types


@given(u'un utilisateur non identifié sur le Shopozor')
def step_impl(context):
    context.test.assertFalse(hasattr(context.test.client, 'token'))


@when(u'un client s\'identifie en tant qu\'administrateur avec un e-mail et un mot de passe valides')
def step_impl(context):
    use_fixture(graphql_query, context, 'login.graphql')
    variables = {'email': context.customer['email'], 'password': context.customer['password']}
    response = context.test.client.post_graphql(context.query, variables)
    context.response = get_graphql_content(response)


@then(u'il obtient un message d\'erreur stipulant que ses identifiants sont incorrects')
def step_impl(context):
    token_data = context.response['data']['login']
    context.test.assertIsNone(token_data['token'])
    context.test.assertEqual(token_data['errors']['message'], 'Wrong credentials')


def is_staff(user_type):
    switch = {
        'client': False,
        'administrateur': True
    }
    return switch[user_type]


def valid_mail_and_password(user_type, is_staff_user, context):
    switch = {
        'client': dict(
            email=context.customer['email'],
            password=context.customer['password'],
            isStaff=is_staff_user
        ),
        'administrateur': dict(
            email=context.staff['email'],
            password=context.staff['password'],
            isStaff=is_staff_user
        )
    }
    return switch[user_type]


def invalid_mail_and_password(is_staff_user, context):
    return dict(
        email=context.unknown['email'],
        password=context.unknown['password'],
        isStaff=is_staff_user
    )


@when(
    u'un {user_type:UserType} s\'identifie en tant que {pretended_type:UserType} avec un e-mail et un mot de passe {validity:ValidityType}')
def step_impl(context, user_type, pretended_type, validity):
    use_fixture(graphql_query, context, 'login.graphql')
    if validity:
        variables = valid_mail_and_password(user_type, is_staff(pretended_type), context)
    else:
        variables = invalid_mail_and_password(is_staff(pretended_type), context)
    response = context.test.client.post_graphql(context.query, variables)
    context.response = get_graphql_content(response)


def valid_mail_invalid_password(user_type, is_staff_user, context):
    switch = {
        'client': dict(email=context.customer['email'], password=context.unknown['password'], isStaff=is_staff_user),
        'administrateur': dict(email=context.staff['email'], password=context.unknown['password'],
                               isStaff=is_staff_user)
    }
    return switch[user_type]


@when(
    u'un {user_type:UserType} s\'identifie en tant que {pretended_type:UserType} avec un e-mail valide et un mot de passe invalide')
def step_impl(context, user_type, pretended_type):
    use_fixture(graphql_query, context, 'login.graphql')
    variables = valid_mail_invalid_password(user_type, is_staff(pretended_type), context)
    response = context.test.client.post_graphql(context.query, variables)
    context.response = get_graphql_content(response)


@then(u'il reçoit un token d\'authentification')
def step_impl(context):
    token_data = context.response['data']['login']
    context.test.assertIsNotNone(token_data['token'])
    context.test.assertIsNone(token_data['errors'])

