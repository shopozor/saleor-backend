from django.conf import settings
from django.core.management.base import BaseCommand
from features.utils.graphql.responses_generator import ShopCategoriesGenerator, ShopListsGenerator, ProductListsGenerator


def generate_responses_for_variant(output_folder, variant):

    generator = ShopListsGenerator(output_folder, variant)
    generator.generate()

    generator = ShopCategoriesGenerator(output_folder, variant)
    generator.generate()

    generator = ProductListsGenerator(output_folder, variant)
    generator.generate()


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

        if fixture_variant == 'all':
            for variant in 'small', 'medium', 'large':
                generate_responses_for_variant(output_folder, variant)
        else:
            generate_responses_for_variant(output_folder, fixture_variant)
