# from copy import deepcopy
from django.conf import settings
from django.core.management.base import BaseCommand
# from features.utils.fixtures import json
from features.utils.graphql.responses_generator import ShopCategoriesGenerator, ShopListsGenerator, ProductListsGenerator

# import os


def generate_responses_for_variant(output_folder, variant):
    # os.makedirs(os.path.join(output_folder, variant), exist_ok=True)

    generator = ShopListsGenerator(output_folder, variant)
    generator.generate()

    generator = ShopCategoriesGenerator(output_folder, variant)
    generator.generate()

    generator = ProductListsGenerator(output_folder, variant)
    generator.generate()

    # shop_catalogues, product_details = generate_shop_catalogues(
    #     variant)
    # output_shop_catalogues(shop_catalogues, output_folder, variant)
    # output_product_details(product_details, output_folder, variant)


class Command(BaseCommand):
    help = 'Generate the JSON expected responses to the GraphQL queries tested in the acceptance tests.'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output-folder', type=str, default=settings.GRAPHQL_RESPONSES_FOLDER,
                            help='Folder where to output the JSON files')
        parser.add_argument('--fixture-variant', type=str, default='all',
                            help='Fixture variant: small, medium, large, or all')

    def handle(self, *args, **options):
        output_folder = options['output_folder']
        fixture_variant = options['fixture_variant']
        # os.makedirs(output_folder, exist_ok=True)

        if fixture_variant == 'all':
            for variant in 'small', 'medium', 'large':
                generate_responses_for_variant(output_folder, variant)
        else:
            generate_responses_for_variant(output_folder, fixture_variant)
