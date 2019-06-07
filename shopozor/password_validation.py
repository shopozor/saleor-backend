from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from hashlib import sha1
import re
import requests


class NumberAndLetterValidator:
    def validate(self, password, user=None):
        if not (any(char.isdigit() for char in password) and any(char.isalpha() for char in password)):
            raise ValidationError(
                _("This password must contain at least a number and a letter."),
                code='number_letter_missing',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least a number and a letter."
        )


class SpecialCharacterValidator:
    def validate(self, password, user=None):
        password = "".join(password.split())
        if not re.findall('[^A-Za-z0-9]', password):
            raise ValidationError(
                _("This password must contain at least a special character."),
                code='special_character_missing',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least a special character."
        )


class HasBeenPwndValidator:
    def validate(self, password, user=None):
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
                _("We could not get a correct answer from haveibeenpwnd.com."),
                code='pwnd_not_reachable',
            )

        if(suffix.upper() in response):
            raise ValidationError(
                _("This password has been powned and is not safe anymore."),
                code='password_pwnd',
            )

    def get_help_text(self):
        return _(
            "This password has been powned and is not safe anymore."
        )
