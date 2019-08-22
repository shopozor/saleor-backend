from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from features.utils.fixtures import json
from features.utils.auth.account_handling import create_database_user
from saleor.account.models import User

import os


def load_users_in_database(variant):
    users = []
    for persona in 'Consommateurs', 'Producteurs', 'Responsables', 'Rex', 'Softozor':
        user_data = json.load(os.path.join(
            settings.FIXTURE_DIRS[0], variant, 'Users', persona + '.json'))
        if isinstance(user_data, list):
            for user in user_data:
                stored_user = create_database_user(user)
                assert stored_user.pk == user['id'], '[%s] - %d should equal %d' % (
                    persona, stored_user.pk, user['id'])
                users.append(user)
        else:
            stored_user = create_database_user(user_data)
            assert stored_user.pk == user_data['id'], '[%s] - %d should equal %d' % (
                persona, stored_user.pk, user_data['id'])
            users.append(user_data)
    return users


class Command(BaseCommand):
    help = 'Fills up the database with the relevant data for end-to-end testing.'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--user-output-folder', type=str, default=settings.FIXTURE_DIRS[0],
                            help='Folder where to output the JSON files containing the users and passwords')
        parser.add_argument('--fixture-variant', type=str, default='large',
                            help='Fixture variant: small, medium, or large')

    def handle(self, *args, **options):
        output_folder = options['user_output_folder']
        variant = options['fixture_variant']

        users = load_users_in_database(variant)
        json.dump(users, os.path.join(output_folder, variant, 'Users.json'))

        call_command('loaddata', os.path.join(
            settings.FIXTURE_DIRS[0], variant, 'Shopozor.json'))
