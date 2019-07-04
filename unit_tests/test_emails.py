import pytest
import re

from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.utils.http import urlsafe_base64_decode
from saleor.account.models import User
from shopozor.emails import send_activate_account_email, get_email_base_context


def test_get_email_base_context(site_settings):
    site = site_settings.site
    proper_context = {
        "domain": site.domain,
        "site_name": site.name,
    }

    received_context = get_email_base_context()
    assert proper_context == received_context


def test_send_activate_account_email(customer_user):
    send_activate_account_email(customer_user.pk)
    print(mail.outbox[0].body)
    assert len(mail.outbox) == 1


def test_activate_account_email_correct_url(customer_user):
    send_activate_account_email(customer_user.pk)
    mail_sent = mail.outbox[0].body
    url_split = re.findall(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mail_sent)[0].split('/')

    token = url_split[-1]
    assert default_token_generator.check_token(customer_user, token)

    uid_decoded = urlsafe_base64_decode(url_split[-2]).decode()
    decoded_user = User.objects.get(pk=uid_decoded)
    assert customer_user == decoded_user
