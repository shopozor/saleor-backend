from django.conf import settings
from django.core.management.base import BaseCommand
from features.utils.fixtures import json

from copy import deepcopy

import graphene
import os
import unidecode
import urllib.parse


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
                'id': graphene.Node.to_global_id('Shop', shop_fixture['pk']),
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


def money_amount(price_fields, amount=None):
    return {
        'amount': amount if amount is not None else price_fields['amount'],
        'currency': price_fields['currency']
    }


def get_pricing(variant_fields, product_fields):
    # This method is perfectly fine as long as we don't incorporate taxes
    # When we take taxes into account, we'll need to adapt this method
    # This will document how the taxes are taken into account
    pricing = {}
    if 'price_override' in variant_fields and variant_fields['price_override'] is not None:
        pricing = {
            'price': {
                'gross': money_amount(variant_fields['price_override'])
            }
        }
    else:
        pricing = {
            'price': {
                'gross': money_amount(product_fields['price'])
            }
        }
    return pricing


def set_page_info(query, totalCount):
    query['totalCount'] = totalCount
    query['pageInfo'] = {
        'startCursor': graphene.Node.to_global_id('arrayconnection', 0),
        'endCursor': graphene.Node.to_global_id('arrayconnection', totalCount - 1)
    }


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


def update_product_price_range(product, variant, node):
    variant_pricing = get_pricing(variant['fields'], product['fields'])
    variant_price = variant_pricing['price']
    current_start = node['pricing']['priceRange']['start']
    current_stop = node['pricing']['priceRange']['stop']
    if variant_price['gross']['amount'] < current_start['gross']['amount']:
        return {
            'priceRange': {
                'start': variant_price,
                'stop': current_stop
            }
        }
    elif variant_price['gross']['amount'] > current_stop['gross']['amount']:
        return {
            'priceRange': {
                'start': current_start,
                'stop': variant_price
            }
        }
    else:
        return {
            'priceRange': {
                'start': current_start,
                'stop': current_stop
            }
        }


# def update_product_details(product_details, product_fields, images):
#             'conservation': {
#                 'mode': '',
#                 'duration': ''
#             },
#             'pricing': {
#                 'priceRange': {
#                     'start': {
#                         'gross': money_amount(),
#                         'net': money_amount(),
#                         'tax': money_amount(),
#                     },
#                     'stop': {
#                         'gross': money_amount(),
#                         'net': money_amount(),
#                         'tax': money_amount()
#                     }
#                 }
#             },
#             'purchaseCost': {
#                 'start': money_amount(),
#                 'stop': money_amount()
#             },
#             'variants': [{
#                 'costPrice': money_amount(),
#                 'id': '',
#                 'isAvailable': 0,
#                 'name': '',
#                 'pricing': {
#                     'price': {
#                         'gross': money_amount(),
#                         'net': money_amount(),
#                         'tax': money_amount()
#                     }
#                 },
#                 'sku': '',
#                 'stockQuantity': 0
#             }]

def extract_products_from_catalogues(catalogues):
    result = []
    for shop in catalogues:
        for category in catalogues[shop]:
            for edge in catalogues[shop][category]['data']['products']['edges']:
                node = edge['node']
                product_id = node['id']
                product_already_exists = [
                    product for product in result if product['id'] == product_id]
                if not product_already_exists:
                    # TODO: get rid of the unwanted data
                    node.pop('thumbnail', None)
                    result.append(node)
    return result


def extract_catalogues(catalogues):
    # TODO: get rid of the unwanted data
    for shop in catalogues:
        for category in catalogues[shop]:
            for edge in catalogues[shop][category]['data']['products']['edges']:
                node = edge['node']
                node.pop('description', None)
                node.pop('images', None)
    return catalogues


def generate_shop_catalogues(fixture_variant):
    # TODO: generate conservation { mode, duration }
    # TODO: don't forget to encode the ids!
    # TODO: we need to optimize the access to the images and the variants (--> optimize also the catalogue generation)
    # TODO: to do so, we might need to create a copy of the shops_fixture because we will progressively delete items from it
    shops_fixture = json.load(os.path.join(
        settings.FIXTURE_DIRS[0], fixture_variant, 'Shopozor.json'))
    users_fixture = get_users_fixture(fixture_variant)
    product_catalogues = {}
    for shop in [shop for shop in shops_fixture if shop['model'] == 'shopozor.shop']:
        product_catalogues[shop['pk']] = {}
        for category in [item['pk'] for item in shops_fixture if item['model'] == 'product.category']:
            product_catalogues[shop['pk']][category] = {
                'data': {
                    'products': {
                        'edges': [],
                    }
                }
            }
            totalCount = 0
            catalogue_edges = product_catalogues[shop['pk']
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
                    edge for edge in catalogue_edges if edge['node']['id'] == product['pk']]

                new_variant = {
                    'id': graphene.Node.to_global_id('ProductVariant', variant_id),
                    'name': variant['fields']['name'],
                    'isAvailable': product['fields']['is_published'],
                    'stockQuantity': max(variant['fields']['quantity'] - variant['fields']['quantity_allocated'], 0)
                }
                if edges_with_product_id:
                    # append variant to existing product
                    edge = edges_with_product_id[0]
                    edge['node']['variants'].append(new_variant)
                    edge['node']['pricing'] = update_product_price_range(
                        product, variant, edge['node'])
                else:
                    # create new product with variant
                    staff_ids = [entry['fields']['staff_id'] for entry in shops_fixture if entry['model']
                                 == 'shopozor.productstaff' and entry['fields']['product_id'] == product['pk']]
                    associated_producer = {}
                    if len(staff_ids) > 0:
                        staff_id = staff_ids[0]
                        associated_producer = [{
                            'firstName': user['first_name'],
                            'lastName': user['last_name']
                        } for user in users_fixture if user['id'] == staff_id]
                    associated_images = [{
                        'alt': fixture['fields']['alt'],
                        'url': fixture['fields']['image'],
                    } for fixture in shops_fixture if fixture['model'] == 'product.productimage' and fixture['fields']['product'] == product['pk']]
                    if len(associated_images) == 0:
                        thumbnail = {
                            'alt': None,
                            'url': urllib.parse.urljoin(settings.STATIC_URL, 'images/placeholder%dx%d.png' % (settings.PRODUCT_THUMBNAIL_SIZE, settings.PRODUCT_THUMBNAIL_SIZE))
                        }
                    else:
                        thumbnail = {
                            'alt': associated_images[0]['alt'],
                            'url': urllib.parse.urljoin(settings.MEDIA_URL, '__sized__/%s-thumbnail-%dx%d.%s' % (associated_images[0]['url'].split('.')[0], settings.PRODUCT_THUMBNAIL_SIZE, settings.PRODUCT_THUMBNAIL_SIZE, associated_images[0]['url'].split('.')[1]))
                        }
                    initial_pricing = get_pricing(
                        variant['fields'], product['fields'])
                    initial_price_range = initial_pricing['price']['gross']
                    node = {
                        'node': {
                            'id': graphene.Node.to_global_id('Product', product['pk']),
                            'name': product['fields']['name'],
                            'description': product['fields']['description'],
                            'variants': [new_variant],
                            'images': associated_images,
                            'thumbnail': thumbnail,
                            'productType': {
                                'id': graphene.Node.to_global_id('ProductType', product['fields']['product_type'])
                            },
                            'producer': associated_producer,
                            'pricing': {
                                'priceRange': {
                                    'start': {
                                        'gross': initial_price_range
                                    },
                                    'stop': {
                                        'gross': initial_price_range
                                    }
                                }
                            }
                        }
                    }
                    catalogue_edges.append(node)
                    totalCount += 1

            set_page_info(
                product_catalogues[shop['pk']][category]['data']['products'], totalCount)

    postprocess_is_available_flag(catalogue_edges)
    expected_product_details = extract_products_from_catalogues(
        deepcopy(product_catalogues))
    expected_catalogues = extract_catalogues(deepcopy(product_catalogues))
    return expected_catalogues, expected_product_details


def generate_shop_categories(fixture_variant):
    shops_fixture = json.load(os.path.join(
        settings.FIXTURE_DIRS[0], fixture_variant, 'Shopozor.json'))
    expected_categories = {
        'data': {
            'categories': {
                'edges': [],
            }
        }
    }
    totalCount = 0
    edges = expected_categories['data']['categories']['edges']
    for category in [item for item in shops_fixture if item['model'] == 'product.category']:
        node = {
            'node': {
                'id': graphene.Node.to_global_id('Category', category['pk']),
                'name': category['fields']['name'],
                'description': category['fields']['description'],
                'backgroundImage': {
                    'alt': category['fields']['background_image_alt'],
                    'url': urllib.parse.urljoin(settings.MEDIA_URL, '__sized__/%s-thumbnail-%dx%d-70.%s' % (category['fields']['background_image'].split('.')[0], settings.CATEGORY_THUMBNAIL_SIZE, settings.CATEGORY_THUMBNAIL_SIZE, category['fields']['background_image'].split('.')[1]))
                }
            }
        }
        edges.append(node)
        totalCount += 1
    set_page_info(expected_categories['data']['categories'], totalCount)
    return expected_categories


def output_object_to_json(object, output_dir, output_filename):
    os.makedirs(output_dir, exist_ok=True)
    json.dump(object, os.path.join(output_dir, output_filename))


def output_shop_list(output_dir, variant):
    consumer_output_dir = os.path.join(output_dir, variant, 'Consumer')
    output_object_to_json(generate_shop_list(variant),
                          consumer_output_dir, 'Shops.json')


def output_shop_catalogues(shop_catalogues, output_dir, variant):
    catalogues_output_dir = os.path.join(
        output_dir, variant, 'Consumer', 'Catalogues')
    for catalogue in shop_catalogues:
        for category in shop_catalogues[catalogue]:
            output_object_to_json(
                shop_catalogues[catalogue][category], os.path.join(catalogues_output_dir, 'Shop-%d' % catalogue), 'Category-%d.json' % category)


def output_product_details(product_details, output_dir, variant):
    products_output_dir = os.path.join(
        output_dir, variant, 'Consumer', 'Products')
    for detail in product_details:
        output_object_to_json(
            detail, products_output_dir, 'Product-%d.json' % int(graphene.Node.from_global_id(detail['id'])[1]))


def output_shop_categories(output_dir, variant):
    os.makedirs(os.path.join(output_dir, variant), exist_ok=True)
    categories_output_dir = os.path.join(
        output_dir, variant, 'Consumer'
    )
    output_object_to_json(generate_shop_categories(
        variant), categories_output_dir, 'Categories.json')


class Command(BaseCommand):
    help = 'Generate the JSON expected responses to the GraphQL queries tested in the acceptance tests.'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--output-folder', type=str, default=settings.GRAPHQL_RESPONSES_FOLDER,
                            help='Folder where to output the JSON files')

    def handle(self, *args, **options):
        output_folder = options['output_folder']
        os.makedirs(output_folder, exist_ok=True)
        # for variant in 'small', 'medium', 'large':
        #     os.makedirs(os.path.join(output_folder, variant), exist_ok=True)
        #     output_shop_list(output_folder, variant)
        #     shop_catalogues, product_details = generate_shop_catalogues(
        #         variant)
        #     output_shop_catalogues(shop_catalogues, output_folder, variant)
        #     output_product_details(product_details, output_folder, variant)
        #     output_shop_categories(output_folder, variant)
        variant = 'small'
        os.makedirs(os.path.join(output_folder, variant), exist_ok=True)
        output_shop_list(output_folder, variant)
        shop_catalogues, product_details = generate_shop_catalogues(
            variant)
        output_shop_catalogues(shop_catalogues, output_folder, variant)
        output_product_details(product_details, output_folder, variant)
        output_shop_categories(output_folder, variant)
