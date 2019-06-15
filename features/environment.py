from behave import use_fixture
from behave.fixture import use_fixture_by_tag
from django.contrib.auth.models import AnonymousUser
from features.fixtures import user_accounts, login, signup
from tests.api.conftest import ApiClient

fixtures_registry = {
    'fixture.user-accounts': user_accounts,
    'fixture.login': login,
    'fixture.signup': signup
}


def before_tag(context, tag):
    if tag.startswith("fixture."):
        return use_fixture_by_tag(tag, context, fixtures_registry)


def django_ready(context):
    context.test.client = ApiClient(user=AnonymousUser())
    context.django = True
