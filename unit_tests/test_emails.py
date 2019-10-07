import pytest
import re

from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.utils.http import urlsafe_base64_decode
from saleor.account.models import User
from shopozor.tokens import activation_token_generator
from test_utils.regex_utils import regex_url_uid_token
from test_utils.url_utils import url_activate, url_reset


def test_get_email_base_context(site_settings, email_sender):
    site = site_settings.site
    proper_context = {
        "domain": site.domain,
        "site_name": site.name,
    }

    received_context = email_sender.get_email_base_context()
    assert proper_context == received_context


def test_send_activate_account_email(customer_user, email_sender):
    email_sender.send_activate_account_email(customer_user.pk)
    assert len(mail.outbox) == 1


def test_send_hacker_abuse_email_notification(customer_user, email_sender):
    email_sender.send_hacker_abuse_email_notification(customer_user.email)
    assert len(mail.outbox) == 1


def test_send_password_reset_email(customer_user, email_sender):
    email_sender.send_password_reset(customer_user)
    assert len(mail.outbox) == 1


def test_activate_account_email_correct_url(customer_user, email_sender):
    email_sender.send_activate_account_email(customer_user.pk)
    mail_sent = mail.outbox[0].body
    activate_regex = re.escape(url_activate()) + regex_url_uid_token()
    match = re.search(activate_regex, mail_sent)

    assert activation_token_generator.check_token(
        customer_user, match.group('token'))

    uid_decoded = urlsafe_base64_decode(match.group('uidb64')).decode()
    decoded_user = User.objects.get(pk=uid_decoded)
    assert customer_user == decoded_user


def test_password_reset_email_correct_url(customer_user, email_sender):
    email_sender.send_password_reset(customer_user)
    mail_sent = mail.outbox[0].body
    activate_regex = re.escape(url_reset()) + regex_url_uid_token()
    match = re.search(activate_regex, mail_sent)

    assert default_token_generator.check_token(
        customer_user, match.group('token'))

    uid_decoded = urlsafe_base64_decode(match.group('uidb64')).decode()
    decoded_user = User.objects.get(pk=uid_decoded)
    assert customer_user == decoded_user
