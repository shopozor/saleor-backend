from django.core.management.base import BaseCommand
from features.utils.fixtures.loader import get_data_from_json_fixture
from features.utils.auth.account_handling import create_database_superuser, create_database_user
from saleor.account.models import User

import os


def create_users():
    for persona in 'Consommateurs', 'Producteurs', 'Responsables':
        user_data = get_data_from_json_fixture(os.path.join(
            'features', 'fixtures', 'Authentication', 'Credentials', persona + '.json'))
        for user in user_data:
            create_database_user(user)

    user_data = get_data_from_json_fixture(os.path.join(
        'features', 'fixtures', 'Authentication', 'Credentials', 'Rex.json'))
    create_database_user(user_data)


def create_superusers():
    user_data = get_data_from_json_fixture(os.path.join(
        'features', 'fixtures', 'Authentication', 'Credentials', 'Softozor.json'))
    create_database_superuser(user_data)


class Command(BaseCommand):
    help = 'Fills up the database with the relevant data for end-to-end testing.'

    def handle(self, *args, **options):
        create_users()
        create_superusers()
