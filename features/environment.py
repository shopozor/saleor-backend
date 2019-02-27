from tests.api.conftest import ApiClient
from django.contrib.auth.models import AnonymousUser
from behave import use_fixture
from features.fixtures import *


def before_scenario(context, feature):
    # TODO: use tag information to only load the necessary fixtures
    use_fixture(permissions, context)
    use_fixture(unknown, context)
    use_fixture(consumer, context)
    use_fixture(producer, context)
    use_fixture(manager, context)
    use_fixture(rex, context)
    use_fixture(softozor, context)

    use_fixture(wrong_credentials_response, context)
    use_fixture(user_not_admin_response, context)

    use_fixture(successful_signin, context)
    use_fixture(expired_account_confirmation_link, context)


def after_scenario(context, scenario):
    if hasattr(context, 'query'):
        del context.query


def django_ready(context):
    context.test.client = ApiClient(user=AnonymousUser())
    context.django = True
