from django.core import mail

import re


def check_that_email_was_sent_to_user(test, user_email):
    test.assertEqual(len(mail.outbox), 1)
    sent_email = mail.outbox[0]
    test.assertTrue(user_email in sent_email.recipients())


def gather_email_activation_data(activation_url_prefix):
    mail_handler = ActivationMailHandler(activation_url_prefix)
    sent_email = mail.outbox[0]
    return mail_handler.get_credentials(sent_email.body)


class ActivationMailHandler:
    __url_suffix_pattern = r'\/(?P<uidb64>[0-9A-Za-z_\-]+)\/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})\/'

    def __init__(self, url_prefix):
        self.url_pattern = re.escape(url_prefix) + self.__url_suffix_pattern

    def get_credentials(self, mail_body):
        match = re.search(self.url_pattern, mail_body)
        return None if match is None else self.__extract_credentials_from_regex_match(match)

    def __extract_credentials_from_regex_match(self, match):
        return {'uidb64': match.group('uidb64'), 'token': match.group('token')}
