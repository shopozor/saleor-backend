import os.path

from behave import fixture
from behave.fixture import use_composite_fixture_with, fixture_call_params
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from features.data_factories import ProductFactory, ShopFactory
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
        os.path.join('Authentication', 'Credentials', 'NewConsumer.json'))
    set_password(user_data)
    context.unknown = user_data
    return user_data


@fixture
def consumer(context):
    user_data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Credentials', 'Consommateur.json'))
    set_password(user_data)
    create_database_user(user_data)
    context.consumer = user_data
    return user_data


@fixture
def inactive_customer(context):
    user_data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Credentials', 'InactiveConsumer.json'))
    set_password(user_data)
    create_database_user(user_data)
    context.inactive_customer = user_data
    return user_data


@fixture
def producer(context):
    user_data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Credentials', 'Producteur.json'))
    set_password(user_data)
    create_database_user(user_data)
    context.producer = user_data
    return user_data


@fixture
def manager(context):
    user_data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Credentials', 'Responsable.json'))
    set_password(user_data)
    create_database_user(user_data)
    context.manager = user_data
    return user_data


@fixture
def rex(context):
    user_data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Credentials', 'Rex.json'))
    set_password(user_data)
    create_database_user(user_data)
    context.rex = user_data
    return user_data


@fixture
def softozor(context):
    user_data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Credentials', 'Softozor.json'))
    set_password(user_data)
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
        os.path.join('Authentication', 'LogStaffIn', 'Responses', 'WrongCredentials.json'))
    context.wrong_credentials_response = data
    return data


@fixture
def user_not_admin_response(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'LogStaffIn', 'Responses', 'Consommateur.json'))
    context.user_not_admin_response = data
    return data


@fixture
def failed_query_response(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Logout', 'Responses', 'QueryResponseAfterLogout.json'))
    context.failed_query_response = data
    return data


@fixture
def successful_logout_response(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'Logout', 'Responses', 'Success.json'))
    context.successful_logout_response = data
    return data


@fixture
def successful_signup(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'RegisterConsumer', 'Responses', 'SuccessfulConsumerCreation.json'))
    context.successful_signup = data
    return data


@fixture
def successful_account_confirmation(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'RegisterConsumer', 'Responses', 'SuccessfulAccountConfirmation.json'))
    context.successful_account_confirmation = data
    return data


@fixture
def successful_password_reset(context):
    data = get_data_from_json_fixture(os.path.join(
        'Authentication', 'ResetUserPassword', 'Responses', 'SuccessfulPasswordReset.json'))
    context.successful_password_reset = data
    return data


@fixture
def successful_set_password(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'ResetUserPassword', 'Responses', 'SuccessfulSetPassword.json'))
    context.successful_set_password = data
    return data


@fixture
def password_not_compliant(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'ResetUserPassword', 'Responses', 'PasswordNotCompliant.json'))
    context.password_not_compliant = data
    return data


@fixture
def expired_link(context):
    data = get_data_from_json_fixture(
        os.path.join('Authentication', 'ExpiredLink.json'))
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
    product_factory = ProductFactory(create_images=False)
    product_factory.create()
    shop_factory = ShopFactory()
    shop_factory.create()

# TODO: we want a django command that generates the 'Shops.json' / 'populatedb_data.json' fixture files
# TODO: we want a django command that generates the expected shops list / expected shops catalogues graphql responses
# 1. run command to generate the Shops.json and populatedb_data.json files (always the same files) --> only run once and have those files in version control
# 2. run command to generate the expected shops list and catalogues from the Shops.json and populatedb_data.json fixtures --> also have those files in version control
# 3. read those files here
@fixture
def expected_shop_list(context):
    shops_fixture = get_data_from_json_fixture('Shops.json')
    expected_list = {
        'data': {
            'shops': {
                'edges': []
            }
        }
    }
    for shop_fixture in shops_fixture:
        node = {
            'node': {
                'id': shop_fixture['pk'],
                'name': shop_fixture['fields']['name'],
                'description': shop_fixture['fields']['description'],
                'geocoordinates': {
                    'latitude': shop_fixture['fields']['latitude'],
                    'longitude': shop_fixture['fields']['longitude']
                }
            }
        }
        expected_list['data']['shops']['edges'].append(node)
    context.expected_shop_list = expected_list
    return expected_list


@fixture
def expected_shop_catalogues(context):
    shops_fixture = get_data_from_json_fixture('Shops.json')
    products_fixture = get_data_from_json_fixture(os.path.join(
        '..', '..', 'saleor', 'saleor', 'static', 'populatedb_data.json'))
    expected_catalogues[shop_id] = {
        'data': {
            'shopCatalogue': {
                'products': {
                    'edges': []
                }
            }
        }
    }


@fixture
def shops_fixtures(context):
    return use_composite_fixture_with(context, [fixture_call_params(shops), fixture_call_params(expected_shop_list)])
