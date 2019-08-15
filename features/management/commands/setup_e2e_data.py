from django.conf import settings
from django.core.management.base import BaseCommand
from features.utils.fixtures.loader import get_data_from_json_fixture
from features.utils.auth.account_handling import create_database_superuser, create_database_user
from saleor.account.models import User

import json
import os

# TODO: export all the user data with their passwords
# TODO: in the exported json, make sections grouping the personas together


def create_users():
    users = {}
    for persona in 'Consommateurs', 'Producteurs', 'Responsables', 'Rex':
        users[persona] = []
        user_data = get_data_from_json_fixture(os.path.join(
            'features', 'fixtures', 'Users', persona + '.json'))
        if isinstance(user_data, list):
            for user in user_data:
                create_database_user(user)
                users[persona].append(user)
        else:
            create_database_user(user_data)
            users[persona].append(user_data)
    return users


def create_superusers():
    users = {}
    user_data = get_data_from_json_fixture(os.path.join(
        'features', 'fixtures', 'Users', 'Softozor.json'))
    create_database_superuser(user_data)
    users['Softozor'] = user_data
    return users


class Command(BaseCommand):
    help = 'Fills up the database with the relevant data for end-to-end testing.'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output-folder', type=str, default=settings.FIXTURE_DIRS[0],
                            help='Folder where to output the JSON files containing the users and passwords')

    def handle(self, *args, **options):
        output_folder = options['output_folder']

        users = create_users()
        super_users = create_superusers()

        users.update(super_users)

        with open(os.path.join(output_folder, 'users_with_password.json'), 'w') as json_file:
            json.dump(users, json_file, sort_keys=True)
