from behave import given, then, when, use_fixture
from copy import deepcopy
from datetime import datetime, timedelta
from django.core import mail
from features.utils.auth.account_handling import get_current_encrypted_password, account_exists, is_active_account
from features.utils.auth.credentials_checks import check_compulsory_login_credential_arguments, assertPasswordIsCompliant, assertPasswordIsNotCompliant
from features.utils.auth.mail_confirmation import gather_email_activation_data, check_that_email_was_sent_to_user, check_that_email_is_received_soon_enough, check_compulsory_account_activation_credential_arguments
from features.utils.graphql.loader import get_query_from_file
from freezegun import freeze_time
from saleor.account.models import User
from shopozor.models import HackerAbuseEvents
from test_utils.url_utils import url_activate
from tests.api.utils import get_graphql_content


def signup(client, **kwargs):
    check_compulsory_login_credential_arguments(kwargs)
    query = get_query_from_file('signup.graphql')
    response = client.post_graphql(query, kwargs)
    return get_graphql_content(response)


def activate_account(client, **kwargs):
    check_compulsory_account_activation_credential_arguments(kwargs)
    query = get_query_from_file('activateConsumer.graphql')
    response = client.post_graphql(query, kwargs)
    return get_graphql_content(response)


@given(u'un nouveau Consommateur qui a reçu un lien d\'activation de compte')
def step_impl(context):
    context.current_user = deepcopy(context.unknown)
    test_client = deepcopy(context.test.client)
    context.response = signup(test_client, **context.current_user)
    check_that_email_was_sent_to_user(
        context.test, context.current_user['email'])
    context.credentials = gather_email_activation_data(url_activate())
    context.test.assertIsNotNone(context.credentials)
    context.email_reception_time = datetime.now()


@given(u'qui a déjà activé son compte')
def step_impl(context):
    test_client = deepcopy(context.test.client)
    context.response = activate_account(test_client, **context.credentials)
    context.test.assertEqual(
        context.response['data'], context.successful_account_confirmation['data'])


@when(u'un Consommateur inconnu fait une demande d\'enregistrement avec un mot de passe conforme')
def step_impl(context):
    context.current_user = deepcopy(context.unknown)
    assertPasswordIsCompliant(context.current_user['password'])
    test_client = deepcopy(context.test.client)
    context.response = signup(test_client, **context.current_user)


@when(u'un Consommateur inconnu fait une demande d\'enregistrement avec un mot de passe non conforme')
def step_impl(context):
    context.current_user = deepcopy(context.unknown)
    context.current_user['password'] = 'password'
    assertPasswordIsNotCompliant(
        context.test, context.current_user['password'])
    test_client = deepcopy(context.test.client)
    context.response = signup(test_client, **context.current_user)


@when(u'un utilisateur fait une demande d\'enregistrement avec l\'e-mail d\'un compte inactif et un mot de passe conforme')
def step_impl(context):
    context.current_user = deepcopy(context.inactive_customer)
    assertPasswordIsCompliant(context.current_user['password'])
    test_client = deepcopy(context.test.client)
    context.response = signup(test_client, **context.current_user)


@when(u'un utilisateur fait une demande d\'enregistrement avec l\'e-mail d\'un compte inactif et un mot de passe non conforme')
def step_impl(context):
    context.current_user = deepcopy(context.inactive_customer)
    context.current_encrypted_password = get_current_encrypted_password(
        context.current_user['email'])
    context.current_user['password'] = 'password'
    assertPasswordIsNotCompliant(
        context.test, context.current_user['password'])
    test_client = deepcopy(context.test.client)
    context.response = signup(test_client, **context.current_user)


@when(u'un utilisateur fait une demande d\'enregistrement avec l\'e-mail d\'un compte actif et un mot de passe conforme')
def step_impl(context):
    # in this case, the choice of the password is irrelevant; it must only comply to the password policy
    context.current_user = deepcopy(context.consumer)
    context.current_encrypted_password = get_current_encrypted_password(
        context.current_user['email'])
    assertPasswordIsCompliant(context.current_user['password'])
    test_client = deepcopy(context.test.client)
    context.response = signup(test_client, **context.current_user)


@when(u'il active son compte au plus tard {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    check_that_email_is_received_soon_enough(
        context, expiration_delta_in_seconds)
    test_client = deepcopy(context.test.client)
    context.response = activate_account(test_client, **context.credentials)


@when(u'il active son compte {amount:d} {unit:DurationInSecondsType} après sa réception')
def step_impl(context, amount, unit):
    expiration_delta_in_seconds = amount * unit
    datetime_after_expiration = context.email_reception_time + \
        timedelta(seconds=expiration_delta_in_seconds)
    with freeze_time(datetime_after_expiration):
        test_client = deepcopy(context.test.client)
        context.response = activate_account(test_client, **context.credentials)


@when(u'il l\'active pour la deuxième fois avant l\'expiration du lien')
def step_impl(context):
    # we don't need to check that the link hasn't expired
    # because we are guaranteed to have waited a very little
    # amount of time here
    test_client = deepcopy(context.test.client)
    context.response = activate_account(test_client, **context.credentials)


@then(u'il reçoit un e-mail avec un lien d\'activation de compte')
def step_impl(context):
    context.test.assertEqual(context.successful_signup, context.response)
    check_that_email_was_sent_to_user(
        context.test, context.current_user['email'])
    credentials = gather_email_activation_data(url_activate())
    context.test.assertIsNotNone(credentials)


@then(u'il obtient un message d\'erreur stipulant que son mot de passe n\'est pas conforme à la politique des mots de passe')
def step_impl(context):
    expected_error = {
        'field': None,
        'message': 'PASSWORD_NOT_COMPLIANT'
    }
    context.test.assertTrue(
        expected_error in context.response['data']['consumerCreate']['errors'])


@then(u'son compte est créé')
def step_impl(context):
    context.test.assertEqual(
        len(context.response['data']['consumerCreate']['errors']), 0)
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
    context.test.assertEqual(0, len(mail.outbox))


@then(u'un message d\'avertissement est envoyé à cet e-mail')
def step_impl(context):
    check_that_email_was_sent_to_user(
        context.test, context.current_user['email'])


@then(u'l\'incident est enregistré dans un journal')
def step_impl(context):
    entry = HackerAbuseEvents.objects.latest('timestamp')
    context.test.assertEqual(context.current_user['email'], entry.user.email)


@then(u'son compte est activé')
def step_impl(context):
    context.test.assertEqual(
        context.response, context.successful_account_confirmation)
    context.test.assertTrue(is_active_account(context.current_user['email']))


@then(u'son mot de passe est sauvegardé')
def step_impl(context):
    user = User.objects.filter(email=context.current_user['email']).get()
    context.test.assertTrue(user.password)


@then(u'son mot de passe n\'est pas sauvegardé')
def step_impl(context):
    context.test.assertEqual(get_current_encrypted_password(
        context.current_user['email']), context.current_encrypted_password)


@then(u'il n\'est pas identifié')
def step_impl(context):
    context.test.assertFalse(
        'token' in context.response['data']['consumerActivate'])


@then(u'son lien d\'activation est invalidé')
def step_impl(context):
    test_client = deepcopy(context.test.client)
    response = activate_account(test_client, **context.credentials)
    context.test.assertEqual(
        context.expired_account_confirmation_link, response)


@then(u'il obtient un message d\'erreur stipulant que le lien a expiré')
def step_impl(context):
    context.test.assertEqual(
        context.expired_account_confirmation_link, context.response)
