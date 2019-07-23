from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


INVALID_TOKEN = "LINK_EXPIRED"


class ActivationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.is_active) + super()._make_hash_value(user, timestamp)


activation_token_generator = ActivationTokenGenerator()
