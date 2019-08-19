from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from features.faker.fixtures_faker import UserFactory
from features.utils.fixtures import json

import os


class Command(BaseCommand):
    help = 'Generates the relevant django fixtures for the sake of acceptance testing.'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output-folder', type=str, default=settings.FIXTURE_DIRS[0],
                            help='Folder where to output the JSON files containing the users and passwords')

    def handle(self, *args, **options):
        output_folder = options['output_folder']

        consumers = UserFactory.create_consumers(1000)
        json.dump(consumers, os.path.join(
            output_folder, 'Users', 'Consommateurs.json'))

        producers = UserFactory.create_producers(100)
        json.dump(producers, os.path.join(
            output_folder, 'Users', 'Producteurs.json'))

        managers = UserFactory.create_managers(10)
        json.dump(managers, os.path.join(
            output_folder, 'Users', 'Responsables.json'))

        # TODO: link producers with products
