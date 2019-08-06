import os.path

from behave import fixture
from behave.fixture import use_composite_fixture_with, fixture_call_params
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from features.utils.auth.account_handling import create_database_superuser, create_database_user
from features.utils.auth.password_generation import set_password
from features.utils.fixtures.loader import get_data_from_json_fixture
from features.utils.graphql.loader import get_query_from_file
from saleor.account.models import User
from shopozor.permissions import add_permissions


@fixture
def permissions(context):
    add_permissions(User, Permission, ContentType)


@fixture
def unknown(context):
    user_data = get_data_from_json_fixture(
        os.path.join('features', 'fixtures', 'Users', 'NewConsumer.json'))
    set_password(user_data)
    context.unknown = user_data
    return user_data


@fixture
def consumer(context):
    user_data = get_data_from_json_fixture(
        os.path.join('features', 'fixtures', 'Users', 'Consommateurs.json'))[0]
    create_database_user(user_data)
    context.consumer = user_data
    return user_data


@fixture
def inactive_customer(context):
    user_data = get_data_from_json_fixture(
        os.path.join('features', 'fixtures', 'Users', 'InactiveConsumer.json'))
    create_database_user(user_data)
    context.inactive_customer = user_data
    return user_data


@fixture
def producer(context):
    user_data = get_data_from_json_fixture(
        os.path.join('features', 'fixtures', 'Users', 'Producteurs.json'))[0]
    create_database_user(user_data)
    context.producer = user_data
    return user_data


@fixture
def manager(context):
    user_data = get_data_from_json_fixture(
        os.path.join('features', 'fixtures', 'Users', 'Responsables.json'))[0]
    create_database_user(user_data)
    context.manager = user_data
    return user_data


@fixture
def rex(context):
    user_data = get_data_from_json_fixture(
        os.path.join('features', 'fixtures', 'Users', 'Rex.json'))
    create_database_user(user_data)
    context.rex = user_data
    return user_data


@fixture
def softozor(context):
    user_data = get_data_from_json_fixture(
        os.path.join('features', 'fixtures', 'Users', 'Softozor.json'))
    create_database_superuser(user_data)
    context.softozor = user_data
    return user_data


@fixture
def user_accounts(context):
    # the following fixtures add data to the database
    # therefore they need to be added before each scenario
    # because the database is cleaned up after each scenario
    return use_composite_fixture_with(context,
                                      [fixture_call_params(permissions),
                                       fixture_call_params(consumer),
                                          fixture_call_params(producer),
                                          fixture_call_params(manager),
                                          fixture_call_params(rex),
                                          fixture_call_params(softozor),
                                          fixture_call_params(inactive_customer)])


@fixture
def wrong_credentials_response(context):
    data = get_data_from_json_fixture(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'LogStaffIn', 'WrongCredentials.json'))
    context.wrong_credentials_response = data
    return data


@fixture
def user_not_admin_response(context):
    data = get_data_from_json_fixture(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'LogStaffIn', 'Consommateur.json'))
    context.user_not_admin_response = data
    return data


@fixture
def failed_query_response(context):
    data = get_data_from_json_fixture(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'Logout', 'QueryResponseAfterLogout.json'))
    context.failed_query_response = data
    return data


@fixture
def successful_logout_response(context):
    data = get_data_from_json_fixture(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'Logout', 'Success.json'))
    context.successful_logout_response = data
    return data


@fixture
def successful_signup(context):
    data = get_data_from_json_fixture(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'RegisterConsumer', 'SuccessfulConsumerCreation.json'))
    context.successful_signup = data
    return data


@fixture
def successful_account_confirmation(context):
    data = get_data_from_json_fixture(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'RegisterConsumer', 'SuccessfulAccountConfirmation.json'))
    context.successful_account_confirmation = data
    return data


@fixture
def successful_password_reset(context):
    data = get_data_from_json_fixture(os.path.join(
        settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'ResetUserPassword', 'SuccessfulPasswordReset.json'))
    context.successful_password_reset = data
    return data


@fixture
def successful_set_password(context):
    data = get_data_from_json_fixture(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'ResetUserPassword', 'SuccessfulSetPassword.json'))
    context.successful_set_password = data
    return data


@fixture
def password_not_compliant(context):
    data = get_data_from_json_fixture(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'PasswordNotCompliant.json'))
    context.password_not_compliant = data
    return data


@fixture
def expired_link(context):
    data = get_data_from_json_fixture(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'ExpiredLink.json'))
    context.expired_link = data
    return data


@fixture
def login(context):
    return use_composite_fixture_with(context,
                                      [fixture_call_params(unknown),
                                       fixture_call_params(
                                           wrong_credentials_response),
                                          fixture_call_params(user_not_admin_response)])


@fixture
def signup(context):
    return use_composite_fixture_with(context,
                                      [fixture_call_params(unknown),
                                       fixture_call_params(successful_signup),
                                          fixture_call_params(
                                          expired_link),
                                          fixture_call_params(
                                              successful_account_confirmation)])


@fixture
def password_reset(context):
    return use_composite_fixture_with(context, [fixture_call_params(unknown),
                                                fixture_call_params(
                                                    successful_set_password),
                                                fixture_call_params(
                                                    password_not_compliant),
                                                fixture_call_params(
                                                    expired_link),
                                                fixture_call_params(successful_password_reset)])


@fixture
def shops(context):
    context.fixtures = ['saleor.json', 'Shops.json']


@fixture
def expected_shop_list(context):
    shop_list = get_data_from_json_fixture(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Consumer', 'Shops.json'))
    context.expected_shop_list = shop_list
    return shop_list


@fixture
def expected_shop_catalogues(context):
    catalogues_folder = os.path.join(
        settings.GRAPHQL_RESPONSES_FOLDER, 'Consumer', 'Catalogues')
    catalogues = [os.path.splitext(f)[0] for f in os.listdir(
        catalogues_folder) if os.path.isfile(os.path.join(catalogues_folder, f))]
    shop_catalogues = {}
    for catalogue in catalogues:
        shop_id = catalogue.split('-')[1]
        shop_catalogues[shop_id] = get_data_from_json_fixture(os.path.join(settings.GRAPHQL_RESPONSES_FOLDER,
                                                                           'Consumer', 'Catalogues', '{name}.json'.format(name=catalogue)))
    context.expected_shop_catalogues = shop_catalogues
    return shop_catalogues


@fixture
def shops_fixtures(context):
    return use_composite_fixture_with(context, [fixture_call_params(shops), fixture_call_params(expected_shop_list), fixture_call_params(expected_shop_catalogues)])
