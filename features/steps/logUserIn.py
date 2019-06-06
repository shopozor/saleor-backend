from behave import given, then, when
from django.conf import settings

from features.utils import create_database_user
from shopozor.models import MODELS_PERMISSIONS

import features.types
import jwt


@given(u'un utilisateur non identifié sur le Shopozor')
def step_impl(context):
    context.test.assertFalse(hasattr(context.test.client, 'token'))


@given(u'un utilisateur {is_active:ActivityType} et {has_password:WithOrWithoutType} mot de passe')
def step_impl(context, is_active, has_password):
    user_data = {
        'email': 'hacker_abuse@budzons.ch',
        'password': 'password' if has_password else '',
        'is_active': is_active,
        'is_staff': False
    }
    create_database_user(user_data)
    context.user = user_data


@when(u'un client s\'identifie en tant qu\'administrateur avec un e-mail et un mot de passe valides')
def step_impl(context):
    email = context.consumer['email']
    password = context.consumer['password']
    isStaff = True
    user_logger = context.UserLogger
    context.response = user_logger.login(
        email=email, password=password, isStaff=isStaff)


def is_staff(user_type):
    switch = {
        'client': False,
        'administrateur': True
    }
    return switch[user_type]


@when(
    u'un {user_type:UserType} s\'identifie en tant que {pretended_type:UserType} avec un e-mail et un mot de passe {validity:ValidityType}')
def step_impl(context, user_type, pretended_type, validity):
    user_logger = context.UserLogger
    credentials = user_logger.valid_mail_and_password(user_type, is_staff(
        pretended_type)) if validity else user_logger.invalid_mail_and_password(is_staff(pretended_type))
    context.response = user_logger.login(**credentials)


@when(
    u'un {user_type:UserType} s\'identifie en tant que {pretended_type:UserType} avec un e-mail valide et un mot de passe invalide')
def step_impl(context, user_type, pretended_type):
    user_logger = context.UserLogger
    credentials = user_logger.valid_mail_invalid_password(
        user_type, is_staff(pretended_type))
    context.response = user_logger.login(**credentials)


@when(u'un {persona:PersonaType} s\'identifie avec un e-mail et un mot de passe valides')
def step_impl(context, persona):
    user_logger = context.UserLogger
    credentials = user_logger.valid_persona_credentials(persona)
    context.response = user_logger.login(**credentials)


@when(u'il s\'identifie')
def step_impl(context):
    credentials = {
        'email': context.user['email'],
        'password': context.user['password']
    }
    user_logger = context.UserLogger
    context.response = user_logger.login(**credentials)


@then(u'il obtient un message d\'erreur stipulant que ses identifiants sont incorrects')
def step_impl(context):
    context.test.assertEqual(
        context.response['data'], context.wrong_credentials_response['data'])


@then(u'il obtient un message d\'erreur stipulant que son compte n\'a pas les droits d\'administrateur')
def step_impl(context):
    context.test.assertEqual(
        context.response['data'], context.user_not_admin_response['data'])


@then(u'il n\'obtient pas de permissions')
def step_impl(context):
    permissions_data = context.response['data']['login']['user']['permissions']
    context.test.assertEqual(len(permissions_data), 0)


def contains_permission(graphql_permissions, permission):
    return any(perm['code'] == permission for perm in graphql_permissions)


@then(u'il obtient les permissions suivantes')
def step_impl(context):
    permissions_data = context.response['data']['login']['user']['permissions']
    context.test.assertEqual(len(context.table.rows), len(permissions_data))
    for row in context.table:
        expected_permission = row['permission']
        context.test.assertTrue(contains_permission(
            permissions_data, expected_permission))


@then(u'c\'est un super-utilisateur')
def step_impl(context):
    permissions_data = context.response['data']['login']['user']['permissions']
    context.test.assertEqual(len(permissions_data), len(MODELS_PERMISSIONS))
    for permission in MODELS_PERMISSIONS:
        expected_permission = permission.split('.')[1].upper()
        context.test.assertTrue(contains_permission(
            permissions_data, expected_permission))


@then(u'il est considéré comme un {user_type:UserType}')
def step_impl(context, user_type):
    user_data = context.response['data']['login']['user']
    context.test.assertEqual(user_data['isStaff'], is_staff(user_type))


def expiration_delta(token):
    decoded = jwt.decode(token, key=settings.GRAPHQL_JWT['JWT_SECRET_KEY'],
                         algorithm=settings.GRAPHQL_JWT['JWT_ALGORITHM'])
    return decoded['exp'] - decoded['origIat']


@then(u'sa session s\'ouvre pour {amount:d} {unit:DurationInSecondsType}')
def step_impl(context, amount, unit):
    expected_expiration_delta = amount * unit
    token_data = context.response['data']['login']
    token = token_data['token']
    context.test.assertIsNotNone(token)
    context.test.assertEqual(expected_expiration_delta,
                             expiration_delta(token))
    context.test.assertEqual(len(token_data['errors']), 0)
    context.test.assertTrue(settings.GRAPHQL_JWT['JWT_VERIFY_EXPIRATION'])
    context.test.assertEqual(
        settings.GRAPHQL_JWT['JWT_EXPIRATION_DELTA'].total_seconds(), expected_expiration_delta)


# we will assume that django graphql jwt is working as expected
# therefore we don't actually test that the token expires after the specified duration
# instead, we just check that the relevant parameters are set appropriately
@then(u'reste valide pendant {amount:d} {unit:DurationInSecondsType}')
def step_impl(context, amount, unit):
    context.test.assertTrue(settings.GRAPHQL_JWT['JWT_VERIFY_EXPIRATION'])
    context.test.assertEqual(
        settings.GRAPHQL_JWT['JWT_REFRESH_EXPIRATION_DELTA'].total_seconds(), amount * unit)
