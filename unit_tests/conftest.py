from unittest.mock import MagicMock, Mock

import pytest

from django.conf import settings
from django.contrib.sites.models import Site
from shopozor.emails import EmailSender
from saleor.account.models import User
from saleor.site.models import SiteSettings


@pytest.fixture(autouse=True)
def site_settings(db, settings):
    """Create a site and matching site settings.

    This fixture is autouse because django.contrib.sites.models.Site and
    saleor.site.models.SiteSettings have a one-to-one relationship and a site
    should never exist without a matching settings object.
    """
    site = Site.objects.get_or_create(
        name=settings.DOMAIN_NAME, domain=settings.DOMAIN_NAME)[0]
    obj = SiteSettings.objects.get_or_create(site=site)[0]
    settings.SITE_ID = site.pk
    obj.save()
    return obj


@pytest.fixture
def customer_user(db):
    return User.objects.create_user("test@example.com")


@pytest.fixture
def email_sender():
    return EmailSender()
