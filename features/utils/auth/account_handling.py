from django.contrib.auth.models import Permission
from saleor.account.models import User


def create_database_user(user_data):
    is_staff = False if 'is_staff' not in user_data else user_data['is_staff']
    is_active = False if 'is_active' not in user_data else user_data['is_active']
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


def get_current_encrypted_password(email):
    user = User.objects.filter(email=email)
    return user.password


def account_exists(email):
    return User.objects.filter(email=email).count() == 1


def is_active_account(email):
    user = User.objects.filter(email=email)
    return user.is_active
