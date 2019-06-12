from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password, ValidationError
from features.utils.auth.exceptions import UnableToDefineCompliantPassword
from saleor.account.models import User

import random
import string


def create_database_user(user_data):
    is_staff = False if 'isStaff' not in user_data else user_data['isStaff']
    is_active = False if 'isActive' not in user_data else user_data['isActive']
    user = User.objects.create(
        email=user_data['email'], is_staff=is_staff, is_active=is_active)
    if 'password' in user_data:
        user.set_password(user_data['password'])
    if 'permissions' in user_data:
        for permission in user_data['permissions']:
            user.user_permissions.add(Permission.objects.get(
                codename=permission['code'].lower()))
    user.save()
    return user


def create_database_superuser(user_data):
    user = User.objects.create_superuser(email=user_data['email'])
    user.set_password(user_data['password'])
    user.save()


def generate_random_password():
    allowed_chars = ''.join(
        (string.digits, string.ascii_letters, string.punctuation))
    return ''.join(random.choice(allowed_chars) for _ in range(32))


def get_compliant_password():
    maxNbOfAttempts = 10
    nbOfAttempts = 0
    while nbOfAttempts < maxNbOfAttempts:
        password = generate_random_password()
        try:
            validate_password(password)
            return password
        except ValidationError as e:
            nbOfAttempts += 1
            continue
    raise UnableToDefineCompliantPassword(
        'Max allowed number of attempts to generate a random password reached.')


def set_password(user_data):
    user_data['password'] = get_compliant_password()


def get_current_encrypted_password(email):
    user = User.objects.filter(email=email)
    return user.password


def account_exists(email):
    return User.objects.filter(email=email).count() == 1


def is_active_account(email):
    user = User.objects.filter(email=email)
    return user.is_active
