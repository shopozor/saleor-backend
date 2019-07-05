from datetime import datetime
from django.core import mail

import re


def check_that_email_was_sent_to_user(test, user_email):
    test.assertEqual(len(mail.outbox), 1)
    sent_email = mail.outbox[0]
    test.assertTrue(user_email in sent_email.recipients())


def check_that_email_is_received_soon_enough(context, expiration_delta_in_seconds):
    elapsed_time_since_email_reception_in_seconds = (
        datetime.now() - context.email_reception_time).total_seconds()
    context.test.assertTrue(
        elapsed_time_since_email_reception_in_seconds < expiration_delta_in_seconds)


def check_compulsory_account_activation_credential_arguments(kwargs):
    compulsory_args = ('encodedUserId', 'oneTimeToken')
    if not all(key in kwargs for key in compulsory_args):
        raise TypeError(
            'You need to provide at least an encodedUserId and a oneTimeToken')


def check_compulsory_password_reinit_credential_arguments(kwargs):
    compulsory_args = ('encodedUserId', 'oneTimeToken', 'password')
    if not all(key in kwargs for key in compulsory_args):
        raise TypeError(
            'You need to provide at least an encodedUserId, a oneTimeToken, and a password')


def gather_email_activation_data(activation_url_prefix):
    mail_handler = ActivationMailHandler(activation_url_prefix)
    sent_email = mail.outbox[0]
    return mail_handler.get_credentials(sent_email.body)


class ActivationMailHandler:
    __url_suffix_pattern = r'\/(?P<uidb64>[0-9A-Za-z_\-]+)\/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})'

    def __init__(self, url_prefix):
        self.url_pattern = re.escape(url_prefix) + self.__url_suffix_pattern

    def get_credentials(self, mail_body):
        match = re.search(self.url_pattern, mail_body)
        return None if match is None else self.__extract_credentials_from_regex_match(match)

    def __extract_credentials_from_regex_match(self, match):
        return {'encodedUserId': match.group('uidb64'), 'oneTimeToken': match.group('token')}
