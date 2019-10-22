import os.path

from behave import fixture
from behave.fixture import use_composite_fixture_with, fixture_call_params
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from features.utils.auth.account_handling import create_database_user
from features.utils.auth.password_generation import set_password
from features.utils.fixtures import json, database_loader
from features.utils.graphql.loader import get_query_from_file
from saleor.account.models import User
from shopozor.permissions import add_permissions


@fixture
def permissions(context):
    add_permissions(User, Permission, ContentType)


@fixture
def unknown(context):
    user_data = json.load(
        os.path.join(settings.FIXTURE_DIRS[0], 'NewConsumer.json'))
    set_password(user_data)
    context.unknown = user_data
    return user_data


@fixture
def consumer(context):
    user_data = json.load(
        os.path.join(settings.FIXTURE_DIRS[0], 'small', 'Users', 'Consommateurs.json'))[0]
    create_database_user(user_data)
    context.consumer = user_data
    return user_data


@fixture
def inactive_customer(context):
    user_data = json.load(
        os.path.join(settings.FIXTURE_DIRS[0], 'InactiveConsumer.json'))
    create_database_user(user_data)
    context.inactive_customer = user_data
    return user_data


@fixture
def producer(context):
    user_data = json.load(
        os.path.join(settings.FIXTURE_DIRS[0], 'small', 'Users', 'Producteurs.json'))[0]
    create_database_user(user_data)
    context.producer = user_data
    return user_data


@fixture
def manager(context):
    user_data = json.load(
        os.path.join(settings.FIXTURE_DIRS[0], 'small', 'Users', 'Responsables.json'))[0]
    create_database_user(user_data)
    context.manager = user_data
    return user_data


@fixture
def rex(context):
    user_data = json.load(
        os.path.join(settings.FIXTURE_DIRS[0], 'small', 'Users', 'Rex.json'))[0]
    create_database_user(user_data)
    context.rex = user_data
    return user_data


@fixture
def softozor(context):
    user_data = json.load(
        os.path.join(settings.FIXTURE_DIRS[0], 'small', 'Users', 'Softozor.json'))[0]
    create_database_user(user_data)
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
    data = json.load(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'Login', 'WrongCredentials.json'))
    context.wrong_credentials_response = data
    return data


@fixture
def user_not_admin_response(context):
    data = json.load(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'Login', 'Consommateur.json'))
    context.user_not_admin_response = data
    return data


@fixture
def failed_query_response(context):
    data = json.load(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'Logout', 'QueryResponseAfterLogout.json'))
    context.failed_query_response = data
    return data


@fixture
def successful_logout_response(context):
    data = json.load(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'Logout', 'Success.json'))
    context.successful_logout_response = data
    return data


@fixture
def successful_signup(context):
    data = json.load(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'RegisterConsumer', 'SuccessfulConsumerCreation.json'))
    context.successful_signup = data
    return data


@fixture
def successful_account_confirmation(context):
    data = json.load(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'RegisterConsumer', 'SuccessfulAccountConfirmation.json'))
    context.successful_account_confirmation = data
    return data


@fixture
def successful_password_reset(context):
    data = json.load(os.path.join(
        settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'ResetUserPassword', 'SuccessfulPasswordReset.json'))
    context.successful_password_reset = data
    return data


@fixture
def successful_set_password(context):
    data = json.load(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'ResetUserPassword', 'SuccessfulSetPassword.json'))
    context.successful_set_password = data
    return data


@fixture
def signup_password_not_compliant(context):
    data = json.load(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'RegisterConsumer', 'PasswordNotCompliant.json'))
    password_not_compliant = data['data']['consumerCreate']['errors'][0]
    context.password_not_compliant = password_not_compliant
    return password_not_compliant


@fixture
def password_reset_password_not_compliant(context):
    data = json.load(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'ResetUserPassword', 'PasswordNotCompliant.json'))
    password_not_compliant = data['data']['setPassword']['errors'][0]
    context.password_not_compliant = password_not_compliant
    return password_not_compliant


@fixture
def signup_expired_link(context):
    data = json.load(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'RegisterConsumer', 'ExpiredLink.json'))
    expired_link = data['data']['consumerActivate']
    context.expired_link = expired_link
    return expired_link


@fixture
def password_reset_expired_link(context):
    data = json.load(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'Authentication', 'ResetUserPassword', 'ExpiredLink.json'))
    expired_link = data['data']['setPassword']
    context.expired_link = expired_link
    return expired_link


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
                                          signup_expired_link),
                                       fixture_call_params(
                                          successful_account_confirmation),
                                       fixture_call_params(signup_password_not_compliant)])


@fixture
def password_reset(context):
    return use_composite_fixture_with(context, [fixture_call_params(unknown),
                                                fixture_call_params(
                                                    successful_set_password),
                                                fixture_call_params(
                                                    password_reset_password_not_compliant),
                                                fixture_call_params(
                                                    password_reset_expired_link),
                                                fixture_call_params(successful_password_reset)])


@fixture
def small_users_list(context):
    users = database_loader.load_users_in_database('small')
    context.users = users
    return users


@fixture
def small_shops(context):
    context.fixtures = [os.path.join('small', 'Shopozor.json')]


@fixture
def expected_small_shop_list(context):
    shop_list = json.load(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'small', 'Consumer', 'Shops.json'))
    context.expected_shop_list = shop_list
    return shop_list


@fixture
def expected_small_shop_catalogues(context):
    catalogues_folder = os.path.join(
        settings.GRAPHQL_RESPONSES_FOLDER, 'small', 'Consumer', 'Catalogues')
    shops = [shop for shop in os.listdir(catalogues_folder) if os.path.isdir(
        os.path.join(catalogues_folder, shop))]
    shop_catalogues = {}
    for shop in shops:
        shop_id = int(shop.split('-')[1])
        shop_dir = os.path.join(catalogues_folder, shop)
        categories = [category for category in os.listdir(
            shop_dir) if os.path.isfile(os.path.join(shop_dir, category))]
        shop_catalogues[shop_id] = {}
        for category in categories:
            category_id = int(category.split('.')[0].split('-')[1])
            shop_catalogues[shop_id][category_id] = json.load(os.path.join(
                catalogues_folder, shop, category))
    context.expected_shop_catalogues = shop_catalogues
    return shop_catalogues


@fixture
def expected_small_shop_categories(context):
    categories = json.load(os.path.join(
        settings.GRAPHQL_RESPONSES_FOLDER, 'small', 'Consumer', 'Categories.json'))
    context.expected_categories = categories
    return categories


@fixture
def expected_small_product_details(context):
    products_folder = os.path.join(
        settings.GRAPHQL_RESPONSES_FOLDER, 'small', 'Consumer', 'Products')
    product_details_filenames = [item for item in os.listdir(products_folder) if os.path.isfile(
        os.path.join(products_folder, item))]
    product_details = {}
    for filename in product_details_filenames:
        product_id = int(filename.split('.')[0].split('-')[1])
        product_details[product_id] = json.load(os.path.join(
            products_folder, filename))
    context.expected_product_details = product_details
    return product_details


@fixture
def small_shops_fixtures(context):
    return use_composite_fixture_with(context,
                                      [fixture_call_params(permissions),
                                       fixture_call_params(small_users_list),
                                          fixture_call_params(small_shops),
                                          fixture_call_params(
                                              expected_small_shop_list),
                                          fixture_call_params(
                                              expected_small_shop_catalogues),
                                          fixture_call_params(
                                              expected_small_shop_categories),
                                          fixture_call_params(expected_small_product_details)])


@fixture
def tiny_users_list(context):
    users = database_loader.load_users_in_database('tiny')
    context.users = users
    return users


@fixture
def tiny_shops(context):
    context.fixtures = [os.path.join('tiny', 'Shopozor.json')]


@fixture
def expected_tiny_shop_list(context):
    shop_list = json.load(
        os.path.join(settings.GRAPHQL_RESPONSES_FOLDER, 'tiny', 'Consumer', 'Shops.json'))
    context.expected_shop_list = shop_list
    return shop_list


@fixture
def expected_tiny_shop_catalogues(context):
    catalogues_folder = os.path.join(
        settings.GRAPHQL_RESPONSES_FOLDER, 'tiny', 'Consumer', 'Catalogues')
    shops = [shop for shop in os.listdir(catalogues_folder) if os.path.isdir(
        os.path.join(catalogues_folder, shop))]
    shop_catalogues = {}
    for shop in shops:
        shop_id = int(shop.split('-')[1])
        shop_dir = os.path.join(catalogues_folder, shop)
        categories = [category for category in os.listdir(
            shop_dir) if os.path.isfile(os.path.join(shop_dir, category))]
        shop_catalogues[shop_id] = {}
        for category in categories:
            category_id = int(category.split('.')[0].split('-')[1])
            shop_catalogues[shop_id][category_id] = json.load(os.path.join(
                catalogues_folder, shop, category))
    context.expected_shop_catalogues = shop_catalogues
    return shop_catalogues


@fixture
def expected_tiny_shop_categories(context):
    categories = json.load(os.path.join(
        settings.GRAPHQL_RESPONSES_FOLDER, 'tiny', 'Consumer', 'Categories.json'))
    context.expected_categories = categories
    return categories


@fixture
def expected_tiny_product_details(context):
    products_folder = os.path.join(
        settings.GRAPHQL_RESPONSES_FOLDER, 'tiny', 'Consumer', 'Products')
    product_details_filenames = [item for item in os.listdir(products_folder) if os.path.isfile(
        os.path.join(products_folder, item))]
    product_details = {}
    for filename in product_details_filenames:
        product_id = int(filename.split('.')[0].split('-')[1])
        product_details[product_id] = json.load(os.path.join(
            products_folder, filename))
    context.expected_product_details = product_details
    return product_details


@fixture
def tiny_shops_fixtures(context):
    return use_composite_fixture_with(context,
                                      [fixture_call_params(permissions),
                                       fixture_call_params(tiny_users_list),
                                          fixture_call_params(tiny_shops),
                                          fixture_call_params(
                                              expected_tiny_shop_list),
                                          fixture_call_params(
                                              expected_tiny_shop_catalogues),
                                          fixture_call_params(
                                              expected_tiny_shop_categories),
                                          fixture_call_params(expected_tiny_product_details)])
