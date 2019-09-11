from django.contrib.auth.models import Permission
from features.utils.auth.password_generation import set_password
from saleor.account.models import User, Address


def create_database_user(user_data):
    is_superuser = user_data['isSuperUser']
    if is_superuser:
        user = User.objects.create_superuser(
            email=user_data['email'], pk=user_data['id'])
    else:
        is_staff = user_data['isStaff']
        is_active = user_data['isActive']
        user = User.objects.create(
            email=user_data['email'], is_staff=is_staff, is_active=is_active, pk=user_data['id'])

    if 'password' not in user_data:
        set_password(user_data)

    if all(key in user_data for key in ('lastName', 'firstName')):
        user.first_name = user_data['firstName']
        user.last_name = user_data['lastName']

    if 'address' in user_data:
        user_address = user_data['address']
        street_address = user_address.get('streetAddress', '')
        address = Address.objects.create(city=user_address['city'], street_address_1=street_address, postal_code=user_address['postalCode'], country=user_address['country'])
        user.addresses.add(address)

    user.set_password(user_data['password'])

    if 'permissions' in user_data:
        for permission in user_data['permissions']:
            user.user_permissions.add(Permission.objects.get(
                codename=permission['code'].lower()))

    user.save()

    return user


def get_current_encrypted_password(email):
    user = User.objects.filter(email=email).get()
    return user.password


def account_exists(email):
    return User.objects.filter(email=email).count() == 1


def is_active_account(email):
    user = User.objects.filter(email=email).get()
    return user.is_active
