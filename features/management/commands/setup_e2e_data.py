from django.core.management.base import BaseCommand
from features.utils.fixtures.loader import get_data_from_json_fixture
from features.utils.auth.account_handling import create_database_superuser, create_database_user
from saleor.account.models import User

import os


def create_users():
    for persona in 'Consommateurs', 'Producteurs', 'Responsables', 'Rex':
        user_data = get_data_from_json_fixture(os.path.join(
            'features', 'fixtures', 'Users', persona + '.json'))
        if isinstance(user_data, list):
            for user in user_data:
                create_database_user(user)
        else:
            create_database_user(user_data)


def create_superusers():
    user_data = get_data_from_json_fixture(os.path.join(
        'features', 'fixtures', 'Users', 'Softozor.json'))
    create_database_superuser(user_data)


class Command(BaseCommand):
    help = 'Fills up the database with the relevant data for end-to-end testing.'

    def handle(self, *args, **options):
        create_users()
        create_superusers()
