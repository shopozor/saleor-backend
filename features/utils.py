import json
import os.path

from django.conf import settings
from django.contrib.auth.models import Permission

from saleor.account.models import User


def get_query_from_file(filename):
    path_to_query = '/'.join([settings.GRAPHQL_QUERIES_FOLDER, filename])
    with open(path_to_query, 'r') as myfile:
        return myfile.read().replace('\n', '')


def get_data_from_json_fixture(filename):
    fixture_filename = os.path.join(settings.FIXTURES_FOLDER, filename)
    with open(fixture_filename) as file:
        data = json.load(file)
    return data


def create_database_user(user_data):
    is_staff = False if 'is_staff' not in user_data else user_data['is_staff']
    user = User.objects.create(email=user_data['email'], is_staff=is_staff)
    user.set_password(user_data['password'])
    if 'permissions' in user_data:
        for permission in user_data['permissions']:
            user.user_permissions.add(Permission.objects.get(codename=permission['code'].lower()))
    user.save()
    return user
