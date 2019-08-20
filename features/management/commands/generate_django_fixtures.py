from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from features.faker.fixtures_faker import UserFactory
from features.utils.fixtures import json

import os

PATH_TO_SALEOR_FIXTURE = os.path.join(settings.FIXTURE_DIRS[0], 'saleor.json')


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

        nb_of_managers = 10
        managers = UserFactory.create_managers(nb_of_managers)
        json.dump(managers, os.path.join(
            output_folder, 'Users', 'Responsables.json'))

        rex = UserFactory.create_rex()
        json.dump(rex, os.path.join(
            output_folder, 'Users', 'Rex.json'))

        softozor = UserFactory.create_softozor()
        json.dump(softozor, os.path.join(
            output_folder, 'Users', 'Softozor.json'))

        # TODO: link producers with products ==> generate the Shops.json django fixture
        saleor_fixture = json.load(PATH_TO_SALEOR_FIXTURE)
        products = [item for item in saleor_fixture if item['model']
                    == 'product.product']
        product_variants = [
            item for item in saleor_fixture if item['model'] == 'product.productvariant']
        shops = UserFactory.create_shops(
            producers, products, product_variants, nb_of_managers)
        json.dump(shops, os.path.join(output_folder, '_Shops.json'))
