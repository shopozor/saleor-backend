from behave import use_fixture
from behave.fixture import use_fixture_by_tag
from django.contrib.auth.models import AnonymousUser
from features.fixtures import user_accounts, login, signup, password_reset, shops
from tests.api.conftest import ApiClient

import factory.random

fixtures_registry = {
    'fixture.user-accounts': user_accounts,
    'fixture.login': login,
    'fixture.signup': signup,
    'fixture.password-reset': password_reset,
    'fixture.shops': shops
}


def before_tag(context, tag):
    # TODO: is this the most appropriate time to setup the random factory? that needs to happen before the creation of any fixture
    factory.random.reseed_random('shopozor')
    # factory.Faker._DEFAULT_LOCALE = 'fr_CH'
    if tag.startswith("fixture."):
        return use_fixture_by_tag(tag, context, fixtures_registry)


def django_ready(context):
    context.test.client = ApiClient(user=AnonymousUser())
    context.django = True
