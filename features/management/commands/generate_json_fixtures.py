from django.conf import settings
from django.core.management.base import BaseCommand
from features.utils.fixtures.loader import get_data_from_json_fixture

import json
import os

PATH_TO_SHOPS_FIXTURE = os.path.join('features', 'fixtures', '_Shops.json')
PATH_TO_SALEOR_FIXTURE = os.path.join('features', 'fixtures', 'saleor.json')


def generate_shop_list():
    shops_fixture = get_data_from_json_fixture(PATH_TO_SHOPS_FIXTURE)
    expected_list = {
        'data': {
            'shops': {
                'edges': []
            }
        }
    }
    edges = expected_list['data']['shops']['edges']
    for shop_fixture in shops_fixture:
        fields = shop_fixture['fields']
        node = {
            'node': {
                'id': shop_fixture['pk'],
                'name': fields['name'],
                'description': fields['description'],
                'geocoordinates': {
                    'latitude': fields['latitude'],
                    'longitude': fields['longitude']
                }
            }
        }
        edges.append(node)
    return expected_list


def generate_shop_catalogues():
    shops_fixture = get_data_from_json_fixture(PATH_TO_SHOPS_FIXTURE)
    products_fixture = get_data_from_json_fixture(PATH_TO_SALEOR_FIXTURE)

    expected_catalogues = dict()
    for shop in shops_fixture:
        expected_catalogues[shop['pk']] = {
            'data': {
                'shopCatalogue': {
                    'products': {
                        'edges': []
                    }
                }
            }
        }
        edges = expected_catalogues[shop['pk']
                                    ]['data']['shopCatalogue']['products']['edges']
        for variant_id in shop['fields']['product_variants']:
            variant = [entry for entry in products_fixture if entry['model']
                       == 'product.productvariant' and entry['pk'] == variant_id][0]
            product = [entry for entry in products_fixture if entry['model'] ==
                       'product.product' and entry['pk'] == variant['fields']['product']][0]
            is_published = product['fields']['is_published']
            if not is_published:
                continue
            edges_with_product_id = [
                edge for edge in edges if edge['node']['id'] == product['pk']]
            if edges_with_product_id:
                edge = edges_with_product_id[0]
                new_variant = {
                    'id': variant_id
                }
                edge['node']['variants'].append(new_variant)
            else:
                node = {
                    'node': {
                        'id': product['pk'],
                        'name': product['fields']['name'],
                        'variants': [{
                            'id': variant_id
                        }]
                    }
                }
                edges.append(node)
    return expected_catalogues


def output_object_to_json(object, output_dir, output_filename):
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, output_filename), 'w') as json_file:
        json.dump(object, json_file, sort_keys=True, indent=2)
        json_file.write('\n')


def output_shop_list(output_dir):
    consumer_output_dir = os.path.join(output_dir, 'Consumer')
    output_object_to_json(generate_shop_list(),
                          consumer_output_dir, 'Shops.json')


def output_shop_catalogues(output_dir):
    catalogues_output_dir = os.path.join(output_dir, 'Consumer', 'Catalogues')
    shop_catalogues = generate_shop_catalogues()
    for catalogue in shop_catalogues:
        output_object_to_json(
            shop_catalogues[catalogue], catalogues_output_dir, 'Shop-{id}.json'.format(id=catalogue))


class Command(BaseCommand):
    help = 'Generate the JSON expected responses to the GraphQL queries tested in the acceptance tests.'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output-folder', type=str, default=settings.GRAPHQL_RESPONSES_FOLDER,
                            help='Folder where to output the JSON files')

    def handle(self, *args, **options):
        output_folder = options['output_folder']
        os.makedirs(output_folder, exist_ok=True)
        output_shop_list(output_folder)
        output_shop_catalogues(output_folder)


# TODO: we need some products in the saleor database that have is_published == false
# TODO: get the producers from the users_fixture
