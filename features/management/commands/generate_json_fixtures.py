from django.conf import settings
from django.core.management.base import BaseCommand
from features.utils.fixtures.loader import get_data_from_json_fixture

import json
import os

PATH_TO_SALEOR_FIXTURE = os.path.join('features', 'fixtures', 'saleor.json')
PATH_TO_SHOPS_FIXTURE = os.path.join('features', 'fixtures', 'Shops.json')
PATH_TO_USERS_FIXTURE = os.path.join('features', 'fixtures', 'Users.json')


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
    for shop_fixture in [shop for shop in shops_fixture if shop['model'] == 'shopozor.shop']:
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


def postprocess_is_available_flag(edges):
    for edge in edges:
        # an edge is more or less a product
        has_stock = any(variant['stockQuantity'] >
                        0 for variant in edge['node']['variants'])
        for variant in edge['node']['variants']:
            # a variant is available <==> product is visible and has stock
            # a product has stock <==> any of its variant has stock
            variant['isAvailable'] = variant['isAvailable'] and has_stock


def get_pricing(variant_fields, product_fields):
    # This method is perfectly fine as long as we don't incorporate taxes
    # When we take taxes into account, we'll need to adapt this method
    # This will document how the taxes are taken into account
    pricing = {}
    if 'price_override' in variant_fields and variant_fields['price_override'] is not None:
        pricing = {
            'price': {
                'gross': {
                    'currency': variant_fields['price_override']['currency'],
                    'amount': variant_fields['price_override']['amount'],
                }
            }
        }
    else:
        pricing = {
            'price': {
                'gross': {
                    'currency': product_fields['price']['currency'],
                    'amount': product_fields['price']['amount'],
                }
            }
        }
    return pricing


def generate_shop_catalogues():
    shops_fixture = get_data_from_json_fixture(PATH_TO_SHOPS_FIXTURE)
    products_fixture = get_data_from_json_fixture(PATH_TO_SALEOR_FIXTURE)

    expected_catalogues = dict()
    for shop in [shop for shop in shops_fixture if shop['model'] == 'shopozor.shop']:
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

            new_variant = {
                'id': variant_id,
                'name': variant['fields']['name'],
                'isAvailable': product['fields']['is_published'],
                'stockQuantity': max(variant['fields']['quantity'] - variant['fields']['quantity_allocated'], 0),
                'pricing': get_pricing(variant['fields'], product['fields'])
            }
            if edges_with_product_id:
                edge = edges_with_product_id[0]
                edge['node']['variants'].append(new_variant)
            else:
                node = {
                    'node': {
                        'id': product['pk'],
                        'name': product['fields']['name'],
                        'variants': [new_variant],
                        'images': [{
                            'id': fixture['pk'],
                            'alt': fixture['fields']['alt'],
                            # TODO: url needs to be of the form http://localhost:8000/media/products/saleordemoproduct_fd_juice_06_JwLMquZ.png, so we need
                            # to figure out where the http://localhost:8000/media/ is coming from
                            'url': fixture['fields']['image'],
                        } for fixture in products_fixture if fixture['model'] == 'product.productimage' and fixture['fields']['product'] == product['pk']],
                        'category': {
                            'id': product['fields']['category']
                        },
                        'productType': {
                            'id': product['fields']['product_type']
                        },
                        # producer firstName lastName
                    }
                }
                edges.append(node)

    postprocess_is_available_flag(edges)

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
# TODO: generate product images automatically and put them in the /media/products/ folder
