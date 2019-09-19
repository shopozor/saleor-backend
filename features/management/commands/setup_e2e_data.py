from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from features.utils.fixtures import json, database_loader
from saleor.account.models import User

import os


class Command(BaseCommand):
    help = 'Fills up the database with the relevant data for end-to-end testing.'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--user-output-folder', type=str, default=settings.FIXTURE_DIRS[0],
                            help='Folder where to output the JSON files containing the users and passwords')
        parser.add_argument('--fixture-variant', type=str, default='large',
                            help='Fixture variant: tiny, small, medium, or large')

    def handle(self, *args, **options):
        output_folder = options['user_output_folder']
        variant = options['fixture_variant']

        users = database_loader.load_users_in_database(variant)
        json.dump(users, os.path.join(output_folder, variant, 'Users.json'))

        call_command('loaddata', os.path.join(
            settings.FIXTURE_DIRS[0], variant, 'Shopozor.json'))
