from django.conf import settings
from django.core.management.base import BaseCommand
from features.utils.fixtures.loader import get_data_from_json_fixture

import json
import os


def generate_shop_list():
    shops_fixture = get_data_from_json_fixture('Shops.json')
    expected_list = {
        'data': {
            'shops': {
                'edges': []
            }
        }
    }
    for shop_fixture in shops_fixture:
        node = {
            'node': {
                'id': shop_fixture['pk'],
                'name': shop_fixture['fields']['name'],
                'description': shop_fixture['fields']['description'],
                'geocoordinates': {
                    'latitude': shop_fixture['fields']['latitude'],
                    'longitude': shop_fixture['fields']['longitude']
                }
            }
        }
        expected_list['data']['shops']['edges'].append(node)
    return expected_list


def generate_shop_catalogues():
    shops_fixture = get_data_from_json_fixture('Shops.json')
    products_fixture = get_data_from_json_fixture(os.path.join(
        '..', '..', 'saleor', 'saleor', 'static', 'populatedb_data.json'))
    # TODO: get the producers from the users_fixture

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


class Command(BaseCommand):
    help = 'Generate the JSON expected responses to the GraphQL queries tested in the acceptance tests.'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output-folder', type=str,
                            help='Folder where to output the JSON files')

    def handle(self, *args, **options):
        output_folder = options['output_folder'] if options['output_folder'] else settings.GRAPHQL_RESPONSES_FOLDER

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        consumer_output_dir = os.path.join(output_folder, 'Consumer')
        if not os.path.exists(consumer_output_dir):
            os.makedirs(consumer_output_dir)

        with open(os.path.join(consumer_output_dir, 'Shops.json'), 'w') as json_file:
            json.dump(generate_shop_list(), json_file, sort_keys=True)

        catalogues_output_dir = os.path.join(consumer_output_dir, 'Catalogues')
        if not os.path.exists(catalogues_output_dir):
            os.makedirs(catalogues_output_dir)
        shop_catalogues = generate_shop_catalogues()
        for catalogue in shop_catalogues:
            with open(os.path.join(catalogues_output_dir, 'Shop-{id}.json'.format(id=catalogue)), 'w') as json_file:
                json.dump(shop_catalogues[catalogue],
                          json_file, sort_keys=True)