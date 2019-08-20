from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from features.utils.fixtures import json
from features.utils.auth.account_handling import create_database_user
from saleor.account.models import User

import os


def create_users():
    users = []
    for persona in 'Consommateurs', 'Producteurs', 'Responsables', 'Rex':
        user_data = json.load(os.path.join(
            'features', 'fixtures', 'Users', persona + '.json'))
        if isinstance(user_data, list):
            for user in user_data:
                create_database_user(user)
                users.append(user)
        else:
            create_database_user(user_data)
            users.append(user_data)
    return users


def create_superusers():
    users = []
    user_data = json.load(os.path.join(
        'features', 'fixtures', 'Users', 'Softozor.json'))
    create_database_user(user_data)
    users.append(user_data)
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

        users.extend(super_users)

        json.dump(users, os.path.join(output_folder, 'Users.json'))

        call_command('loaddata', os.path.join(
            settings.FIXTURE_DIRS[0], 'saleor.json'))
        call_command('loaddata', os.path.join(
            settings.FIXTURE_DIRS[0], 'Shops.json'))
