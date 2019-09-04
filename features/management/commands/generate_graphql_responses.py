from django.conf import settings
from django.core.management.base import BaseCommand
from features.utils.fixtures import json

import os
import random
import string
import unidecode


def generate_shop_list(fixture_variant):
    shops_fixture = json.load(os.path.join(
        settings.FIXTURE_DIRS[0], fixture_variant, 'Shopozor.json'))
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


def get_users_fixture(fixture_variant):
    users_fixture = json.load(os.path.join(
        settings.FIXTURE_DIRS[0], fixture_variant, 'Users', 'Producteurs.json'))
    users_fixture.extend(json.load(os.path.join(
        settings.FIXTURE_DIRS[0], fixture_variant, 'Users', 'Responsables.json')))
    users_fixture.extend(json.load(os.path.join(
        settings.FIXTURE_DIRS[0], fixture_variant, 'Users', 'Rex.json')))
    users_fixture.extend(json.load(os.path.join(
        settings.FIXTURE_DIRS[0], fixture_variant, 'Users', 'Softozor.json')))
    return users_fixture


def generate_shop_catalogues(fixture_variant):
    shops_fixture = json.load(os.path.join(
        settings.FIXTURE_DIRS[0], fixture_variant, 'Shopozor.json'))
    users_fixture = get_users_fixture(fixture_variant)
    expected_catalogues = dict()
    for shop in [shop for shop in shops_fixture if shop['model'] == 'shopozor.shop']:
        expected_catalogues[shop['pk']] = {}
        for category in [item['pk'] for item in shops_fixture if item['model'] == 'product.category']:
            expected_catalogues[shop['pk']][category] = {
                'data': {
                    'products': {
                        'totalCount': 0,
                        'edges': [],
                        'pageInfo': {
                            'startCursor': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
                            'endCursor': ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                        }
                    }
                }
            }
            totalCount = 0
            edges = expected_catalogues[shop['pk']
                                        ][category]['data']['products']['edges']
            for variant_id in shop['fields']['product_variants']:
                variant = [entry for entry in shops_fixture if entry['model']
                           == 'product.productvariant' and entry['pk'] == variant_id][0]
                product_in_category = [entry for entry in shops_fixture if entry['model'] ==
                                       'product.product' and entry['pk'] == variant['fields']['product'] and entry['fields']['category'] == category]
                if len(product_in_category) == 0:
                    continue
                product = product_in_category[0]
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
                    staff_ids = [entry['fields']['staff_id'] for entry in shops_fixture if entry['model']
                                 == 'shopozor.productstaff' and entry['fields']['product_id'] == product['pk']]
                    associated_producer = {}
                    if len(staff_ids) > 0:
                        staff_id = staff_ids[0]
                        associated_producer = [{
                            'firstName': user['first_name'],
                            'lastName': user['last_name']
                        } for user in users_fixture if user['id'] == staff_id]
                    node = {
                        'node': {
                            'id': product['pk'],
                            'name': product['fields']['name'],
                            'variants': [new_variant],
                            'images': [{
                                'id': fixture['pk'],
                                'alt': fixture['fields']['alt'],
                                'url': fixture['fields']['image'],
                            } for fixture in shops_fixture if fixture['model'] == 'product.productimage' and fixture['fields']['product'] == product['pk']],
                            'productType': {
                                'id': product['fields']['product_type']
                            },
                            'producer': associated_producer
                        }
                    }
                    edges.append(node)
                    totalCount += 1

            expected_catalogues[shop['pk']
                                ][category]['data']['products']['totalCount'] = totalCount

    postprocess_is_available_flag(edges)

    return expected_catalogues


def output_object_to_json(object, output_dir, output_filename):
    os.makedirs(output_dir, exist_ok=True)
    json.dump(object, os.path.join(output_dir, output_filename))


def output_shop_list(output_dir, variant):
    os.makedirs(os.path.join(output_dir, variant), exist_ok=True)
    consumer_output_dir = os.path.join(output_dir, variant, 'Consumer')
    output_object_to_json(generate_shop_list(variant),
                          consumer_output_dir, 'Shops.json')


def output_shop_catalogues(output_dir, variant):
    os.makedirs(os.path.join(output_dir, variant), exist_ok=True)
    catalogues_output_dir = os.path.join(
        output_dir, variant, 'Consumer', 'Catalogues')
    shop_catalogues = generate_shop_catalogues(variant)
    for catalogue in shop_catalogues:
        for category in shop_catalogues[catalogue]:
            output_object_to_json(
                shop_catalogues[catalogue][category], os.path.join(catalogues_output_dir, 'Shop-%d' % catalogue), 'Category-%d.json' % category)


class Command(BaseCommand):
    help = 'Generate the JSON expected responses to the GraphQL queries tested in the acceptance tests.'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output-folder', type=str, default=settings.GRAPHQL_RESPONSES_FOLDER,
                            help='Folder where to output the JSON files')

    def handle(self, *args, **options):
        output_folder = options['output_folder']
        os.makedirs(output_folder, exist_ok=True)
        for variant in 'small', 'medium', 'large':
            output_shop_list(output_folder, variant)
            output_shop_catalogues(output_folder, variant)
