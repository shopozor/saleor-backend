from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from features.faker.fixtures_faker import FakeDataFactory
from features.utils.fixtures import json

import os


variants = {
    'tiny': {
        '#consumers': 1,
        '#producers': 1,
        '#managers': 1,
        '#rex': 1,
        '#softozor': 1,
        '#products': 1,
        '#shops': 1,
        '#max(variants/product)': 1,
        '#max(producers/shop)': 1,
        '#max(products/producer)': 1
    },
    'small': {
        '#consumers': 50,
        '#producers': 16,
        '#managers': 2,
        '#rex': 1,
        '#softozor': 1,
        '#products': 160,
        '#shops': 2,
        '#max(variants/product)': 5,
        '#max(producers/shop)': 8,
        '#max(products/producer)': 10
    },
    'medium': {
        '#consumers': 100,
        '#producers': 30,
        '#managers': 5,
        '#rex': 1,
        '#softozor': 1,
        '#products': 300,
        '#shops': 5,
        '#max(variants/product)': 5,
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
        '#shops': 20,
        '#max(variants/product)': 7,
        '#max(producers/shop)': 7,
        '#max(products/producer)': 25
    }
}


def generate_variant(variant_name, output_folder):

    print('#############################################')
    print('Generating data for %s variant' % variant_name)

    variant = variants[variant_name]
    os.makedirs(os.path.join(output_folder, variant_name), exist_ok=True)
    os.makedirs(os.path.join(output_folder,
                             variant_name, 'Users'), exist_ok=True)

    factory = FakeDataFactory(
        variant['#max(products/producer)'], variant['#max(producers/shop)'], variant['#max(variants/product)'])

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

    shopozor_products = factory.create_shopozor_products(products)
    shopozor.extend(shopozor_products)

    product_variants = factory.create_productvariants(products)
    shopozor.extend(product_variants)

    product_ids = [product['pk'] for product in products]
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

    print('#############################################')


class Command(BaseCommand):
    help = 'Generates the relevant django fixtures for the sake of acceptance testing.'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output-folder', type=str, default=settings.FIXTURE_DIRS[0],
                            help='Folder where to output the JSON files containing the users and passwords')
        parser.add_argument('--fixture-variant', type=str, default='all',
                            help='Fixture variant: tiny, small, medium, large, or all')

    def handle(self, *args, **options):
        output_folder = options['output_folder']
        fixture_variant = options['fixture_variant']

        if fixture_variant == 'all':
            for variant in 'tiny', 'small', 'medium', 'large':
                generate_variant(variant, output_folder)
        else:
            generate_variant(fixture_variant, output_folder)
