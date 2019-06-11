def check_compulsory_credential_arguments(kwargs):
    compulsory_args = ('email', 'password')
    if not all(key in kwargs for key in compulsory_args):
        raise TypeError(
            'You need to provide at least an email and a password to login')
