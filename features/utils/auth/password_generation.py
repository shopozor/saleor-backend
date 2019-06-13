from django.contrib.auth.password_validation import validate_password, ValidationError
from features.utils.auth.exceptions import UnableToDefineCompliantPassword

import random
import string


def set_password(user_data):
    password_generator = RandomCompliantPasswordGenerator()
    user_data['password'] = password_generator.get_compliant_password()


class RandomCompliantPasswordGenerator:
    MAX_NB_OF_ATTEMPTS = 10
    PASSWORD_LENGTH = 32

    def get_compliant_password(self):
        nbOfAttempts = 0
        while nbOfAttempts < self.MAX_NB_OF_ATTEMPTS:
            password = self.__generate_random_password()
            try:
                validate_password(password)
                return password
            except ValidationError as e:
                nbOfAttempts += 1
                continue
        raise UnableToDefineCompliantPassword(
            'Max allowed number of attempts to generate a random password reached.')

    def __generate_random_password(self):
        allowed_chars = ''.join(
            (string.digits, string.ascii_letters, string.punctuation))
        return ''.join(random.choice(allowed_chars) for _ in range(self.PASSWORD_LENGTH))
