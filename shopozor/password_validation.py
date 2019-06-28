from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from hashlib import sha1
import re
import requests


class NumberAndLetterValidator:
    def __init__(self):
        self.error_string = "The password must contain at least one number and one letter."
        self.error_code = "number_letter_missing"

    def is_valid_password(self, password):
        return any(char.isdigit() for char in password) and any(char.isalpha() for char in password)

    def validate(self, password, user=None):
        if not self.is_valid_password(password):
            raise ValidationError(
                _(self.error_string),
                code=self.error_code,
            )

    def get_help_text(self):
        return _(
            self.error_string
        )


class SpecialCharacterValidator:
    def __init__(self):
        self.error_string = "The password must contain at least one special character."
        self.error_code = "special_character_missing"

    def is_valid_password(self, password):
        password = "".join(password.split())
        return re.findall('[^A-Za-z0-9]', password)

    def validate(self, password, user=None):
        if not self.is_valid_password(password):
            raise ValidationError(
                _(self.error_string),
                code=self.error_code,
            )

    def get_help_text(self):
        return _(
            self.error_string
        )


class HasBeenPwndValidator:
    def __init__(self):
        self.error_string = "The password has been pawned and is not safe anymore."
        self.error_code = "password_pwnd"
        self.error_not_reachable = "pwnd_not_reachable"

    def is_valid_password(self, password):
        headers = {
            'user-agent': 'pypi.org/project/haveibeenpwnd/ v0.1', 'api-version': 2}
        range_url = 'https://api.pwnedpasswords.com/range/{}'
        hashed_password = sha1(password.encode('utf-8')).hexdigest()
        prefix = hashed_password[:5]
        suffix = hashed_password[5:]
        # only send a prefix of 5 chars to haveibeenpwnd.com
        try:
            response = requests.get(range_url.format(prefix), headers).text
        except requests.exceptions.RequestException:
            raise ValidationError(
                _("We could not get a successful answer from haveibeenpwnd.com."),
                code=self.error_not_reachable,
            )
        return not suffix.upper() in response

    def validate(self, password, user=None):

        if not self.is_valid_password(password):
            raise ValidationError(
                _(self.error_string),
                code=self.error_code,
            )

    def get_help_text(self):
        return _(
            self.error_string
        )
