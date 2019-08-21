from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from features.faker.fixtures_faker import FakeDataFactory
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

        factory = FakeDataFactory()

        nb_of_consumers = 1000
        start_index = 1
        consumers = factory.create_consumers(
            start_index, nb_of_consumers)
        json.dump(consumers, os.path.join(
            output_folder, 'Users', 'Consommateurs.json'))

        nb_of_producers = 100
        start_index += nb_of_consumers
        producers = factory.create_producers(
            start_index, nb_of_producers)
        json.dump(producers, os.path.join(
            output_folder, 'Users', 'Producteurs.json'))

        nb_of_managers = 10
        start_index += nb_of_producers
        managers = factory.create_managers(start_index, nb_of_managers)
        json.dump(managers, os.path.join(
            output_folder, 'Users', 'Responsables.json'))

        nb_of_rex = 1
        start_index += nb_of_managers
        rex = factory.create_rex(start_index)
        json.dump(rex, os.path.join(
            output_folder, 'Users', 'Rex.json'))

        start_index += nb_of_rex
        softozor = factory.create_softozor(start_index)
        json.dump(softozor, os.path.join(
            output_folder, 'Users', 'Softozor.json'))

        staff = factory.create_staff(producers)
        saleor_fixture = json.load(PATH_TO_SALEOR_FIXTURE)
        products = [item for item in saleor_fixture if item['model']
                    == 'product.product']
        productstaff = factory.create_productstaff(producers, products)

        staff.extend(productstaff)

        product_variants = [
            item for item in saleor_fixture if item['model'] == 'product.productvariant']
        print('nbProds    = ', len(products))
        print('nbVariants = ', len(product_variants))
        shops = factory.create_shops(
            producers, productstaff, product_variants, nb_of_managers)

        staff.extend(shops)
        json.dump(staff, os.path.join(output_folder, 'Shops.json'))
