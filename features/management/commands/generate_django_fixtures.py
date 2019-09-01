from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from features.faker.fixtures_faker import FakeDataFactory
from features.utils.fixtures import json

import os


variants = {
    'small': {
        '#consumers': 10,
        '#producers': 5,
        '#managers': 2,
        '#rex': 1,
        '#softozor': 1,
        '#products': 50,
        '#productvariants': 200,
        '#shops': 2,
        '#max(producers/shop)': 2,
        '#max(products/producer)': 10
    },
    'medium': {
        '#consumers': 100,
        '#producers': 30,
        '#managers': 5,
        '#rex': 1,
        '#softozor': 1,
        '#products': 300,
        '#productvariants': 500,
        '#shops': 5,
        '#max(producers/shop)': 6,
        '#max(products/producer)': 10
    },
    'large': {
        '#consumers': 1000,
        '#producers': 150,
        '#managers': 20,
        '#rex': 1,
        '#softozor': 1,
        '#products': 5000,
        '#productvariants': 50000,
        '#shops': 20,
        '#max(producers/shop)': 7,
        '#max(products/producer)': 25
    }
}


def generate_variant(variant_name, output_folder):

    variant = variants[variant_name]
    os.makedirs(os.path.join(output_folder, variant_name), exist_ok=True)
    os.makedirs(os.path.join(output_folder,
                             variant_name, 'Users'), exist_ok=True)

    factory = FakeDataFactory(
        variant['#max(products/producer)'], variant['#max(producers/shop)'])

    nb_of_consumers = variant['#consumers']
    start_index = 1
    consumers = factory.create_consumers(
        start_index, nb_of_consumers)
    json.dump(consumers, os.path.join(
        output_folder, variant_name, 'Users', 'Consommateurs.json'))

    nb_of_producers = variant['#producers']
    start_index += nb_of_consumers
    producers = factory.create_producers(
        start_index, nb_of_producers)
    json.dump(producers, os.path.join(
        output_folder, variant_name, 'Users', 'Producteurs.json'))

    nb_of_managers = variant['#managers']
    start_index += nb_of_producers
    managers = factory.create_managers(start_index, nb_of_managers)
    json.dump(managers, os.path.join(
        output_folder, variant_name, 'Users', 'Responsables.json'))

    nb_of_reges = variant['#rex']
    start_index += nb_of_managers
    rex = factory.create_reges(start_index, nb_of_reges)
    json.dump(rex, os.path.join(
        output_folder, variant_name, 'Users', 'Rex.json'))

    nb_of_softozors = variant['#softozor']
    start_index += nb_of_reges
    softozor = factory.create_softozors(start_index, nb_of_softozors)
    json.dump(softozor, os.path.join(
        output_folder, variant_name, 'Users', 'Softozor.json'))

    shopozor = []

    categories = factory.create_categories()
    shopozor.extend(categories)

    producttypes = factory.create_producttypes()
    shopozor.extend(producttypes)

    products = factory.create_products(
        categories, producttypes, variant['#products'])
    shopozor.extend(products)

    product_ids = [product['pk'] for product in products]
    product_variants = factory.create_productvariants(
        product_ids, variant['#productvariants'])
    shopozor.extend(product_variants)

    product_images = factory.create_productimages(product_ids)
    shopozor.extend(product_images)

    staff = factory.create_staff(producers)
    shopozor.extend(staff)

    productstaff = factory.create_productstaff(producers, products)
    shopozor.extend(productstaff)

    shops = factory.create_shops(
        producers, productstaff, product_variants, variant['#shops'])
    shopozor.extend(shops)

    json.dump(shopozor, os.path.join(
        output_folder, variant_name, 'Shopozor.json'))


class Command(BaseCommand):
    help = 'Generates the relevant django fixtures for the sake of acceptance testing.'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output-folder', type=str, default=settings.FIXTURE_DIRS[0],
                            help='Folder where to output the JSON files containing the users and passwords')

    def handle(self, *args, **options):
        output_folder = options['output_folder']

        for variant in variants:
            generate_variant(variant, output_folder)
