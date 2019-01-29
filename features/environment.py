from tests.api.conftest import ApiClient
from django.contrib.auth.models import AnonymousUser
from behave import use_fixture
from features.fixtures import *


def before_all(context):
    use_fixture(unknown, context)
    use_fixture(consumer, context)
    use_fixture(producer, context)
    use_fixture(manager, context)
    use_fixture(rex, context)
    use_fixture(softozor, context)
    use_fixture(wrong_credentials_response, context)
    use_fixture(user_not_admin_response, context)


def django_ready(context):
    context.test.client = ApiClient(user=AnonymousUser())
    context.django = True
