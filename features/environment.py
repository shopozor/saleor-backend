from tests.api.conftest import ApiClient
from django.contrib.auth.models import AnonymousUser
from behave import use_fixture
from features.fixtures.user_data import customer, unknown, staff


def before_all(context):
    use_fixture(customer, context)
    use_fixture(unknown, context)
    use_fixture(staff, context)


def django_ready(context):
    context.test.client = ApiClient(user=AnonymousUser())
    context.django = True
