from django.contrib.auth.password_validation import validate_password, ValidationError


def check_compulsory_login_credential_arguments(kwargs):
    compulsory_args = ('email', 'password')
    if not all(key in kwargs for key in compulsory_args):
        raise TypeError(
            'You need to provide at least an email and a password')


def assertPasswordIsNotCompliant(test, password):
    with test.assertRaises(ValidationError):
        validate_password(password)


def assertPasswordIsCompliant(password):
    validate_password(password)
