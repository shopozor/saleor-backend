from django.core.management.base import BaseCommand
from features.utils import *


def create_users():
    for persona in 'Consommateur', 'Producteur', 'Responsable', 'Rex':
        user_data = get_data_from_json_fixture(os.path.join('Authentication', 'Credentials', persona + '.json'))
        create_database_user(user_data)


def create_superusers():
    user_data = get_data_from_json_fixture(os.path.join('Authentication', 'Credentials', 'Softozor.json'))
    create_database_superuser(user_data)


class Command(BaseCommand):
    help = 'Incorporates the Personas from our fixtures to the database, i.e. adds a Consommateur, a Producteur, a Responsable, a Rex, and a Softozor User into the database.'

    def handle(self, *args, **options):
        create_users()
        create_superusers()
