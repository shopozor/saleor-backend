from copy import deepcopy
from django.conf import settings
from features.utils.fixtures import json

import graphene
import os
import urllib.parse


def shop_node(shop_id, shop_fields):
    return {
        'node': {
            'id': graphene.Node.to_global_id('Shop', shop_id),
            'name': shop_fields['name'],
            'description': shop_fields['description'],
            'geocoordinates': {
                'latitude': shop_fields['latitude'],
                'longitude': shop_fields['longitude']
            }
        }
    }


def category_node(category_id, category_fields):
    return {
        'node': {
            'id': graphene.Node.to_global_id('Category', category_id),
            'name': category_fields['name'],
            'description': category_fields['description'],
            'backgroundImage': {
                'alt': category_fields['background_image_alt'],
                'url': urllib.parse.urljoin(settings.MEDIA_URL, '__sized__/%s-thumbnail-%dx%d-70.%s' % (category_fields['background_image'].split('.')[0], settings.CATEGORY_THUMBNAIL_SIZE, settings.CATEGORY_THUMBNAIL_SIZE, category_fields['background_image'].split('.')[1]))
            }
        }
    }


def set_page_info(query, totalCount=None):
    query['totalCount'] = totalCount if totalCount is not None else len(
        query['edges'])
    query['pageInfo'] = {
        'startCursor': graphene.Node.to_global_id('arrayconnection', 0),
        'endCursor': graphene.Node.to_global_id('arrayconnection', query['totalCount'] - 1)
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


def get_shopozor_fixture(fixture_variant):
    return json.load(os.path.join(
        settings.FIXTURE_DIRS[0], fixture_variant, 'Shopozor.json'))


def money_amount(price_fields, amount=None):
    return {
        'amount': amount if amount is not None else price_fields['amount'],
        'currency': price_fields['currency']
    }


def get_price(variant_fields, product_fields):
    # This method is perfectly fine as long as we don't incorporate taxes
    # When we take taxes into account, we'll need to adapt this method
    # This will document how the taxes are taken into account
    price = {}
    if 'price_override' in variant_fields and variant_fields['price_override'] is not None:
        price = {
            'gross': money_amount(variant_fields['price_override']),
            'net': money_amount(variant_fields['price_override']),
            'tax': money_amount(variant_fields['price_override'], amount=0)
        }
    else:
        price = {
            'gross': money_amount(product_fields['price']),
            'net': money_amount(product_fields['price']),
            'tax': money_amount(product_fields['price'], amount=0)
        }
    return price


def variant_node(variant_id, variant_fields, product_fields):
    return {
        'id': graphene.Node.to_global_id('ProductVariant', variant_id),
        'name': variant_fields['name'],
        'isAvailable': product_fields['is_published'],
        'stockQuantity': max(variant_fields['quantity'] - variant_fields['quantity_allocated'], 0),
        'costPrice': {
            'amount': variant_fields['cost_price']['amount'],
            'currency': variant_fields['cost_price']['currency']
        },
        'pricing': {
            'price': get_price(variant_fields, product_fields)
        }
    }


def price_range(start, stop):
    return {
        'priceRange': {
            'start': start,
            'stop': stop
        }
    }


def update_product_price_range(product, variant, node):
    variant_price = get_price(variant['fields'], product['fields'])
    current_start = node['pricing']['priceRange']['start']
    current_stop = node['pricing']['priceRange']['stop']
    if variant_price['gross']['amount'] < current_start['gross']['amount']:
        return price_range(variant_price, current_stop)
    elif variant_price['gross']['amount'] > current_stop['gross']['amount']:
        return price_range(current_start, variant_price)
    else:
        return price_range(current_start, current_stop)


def update_product_purchase_cost(variant, node):
    variant_cost = money_amount(variant['fields']['cost_price'])
    current_start = node['purchaseCost']['start']
    current_stop = node['purchaseCost']['stop']
    if variant_cost['amount'] < current_start['amount']:
        return {
            'start': variant_cost,
            'stop': current_stop
        }
    elif variant_cost['amount'] > current_stop['amount']:
        return {
            'start': current_start,
            'stop': variant_cost
        }
    else:
        return {
            'start': current_start,
            'stop': current_stop
        }


def append_variant_to_existing_product(node, new_variant, variant, product):
    node['variants'].append(new_variant)
    node['pricing'] = update_product_price_range(
        product, variant, node)
    node['purchaseCost'] = update_product_purchase_cost(
        variant, node)


def placeholder_product_thumbnail():
    return {
        'alt': None,
        'url': urllib.parse.urljoin(settings.STATIC_URL, 'images/placeholder%dx%d.png' % (settings.PRODUCT_THUMBNAIL_SIZE, settings.PRODUCT_THUMBNAIL_SIZE))
    }


def product_thumbnail(associated_images):
    return {
        'alt': associated_images[0]['alt'],
        'url': urllib.parse.urljoin(settings.MEDIA_URL, '__sized__/%s-thumbnail-%dx%d.%s' % (associated_images[0]['url'].split('.')[0], settings.PRODUCT_THUMBNAIL_SIZE, settings.PRODUCT_THUMBNAIL_SIZE, associated_images[0]['url'].split('.')[1]))
    }


def product_node(product, variant, new_variant, associated_images, associated_producer, conservation, initial_price, thumbnail):
    return {
        'node': {
            'id': graphene.Node.to_global_id('Product', product['pk']),
            'conservation': conservation[0],
            'name': product['fields']['name'],
            'description': product['fields']['description'],
            'variants': [new_variant],
            'images': associated_images,
            'thumbnail': thumbnail,
            'producer': associated_producer,
            'pricing': {
                'priceRange': {
                    'start': initial_price,
                    'stop': initial_price
                }
            },
            'purchaseCost': {
                'start': variant['fields']['cost_price'],
                'stop': variant['fields']['cost_price']
            }
        }
    }


def create_new_product_with_variant(product, variant, new_variant, users_fixture, shops_fixture):
    staff_ids = [entry['fields']['staff_id'] for entry in shops_fixture if entry['model']
                 == 'shopozor.productstaff' and entry['fields']['product_id'] == product['pk']]
    associated_producer = {}
    if len(staff_ids) > 0:
        staff_id = staff_ids[0]
        producer_descr = [item['fields']['description'] for item in shops_fixture if item['model']
                          == 'shopozor.staff' and item['fields']['user_id'] == staff_id][0]
        associated_producer = [{
            'id': graphene.Node.to_global_id('User', user['id']),
            'description': producer_descr,
            'firstName': user['firstName'],
            'lastName': user['lastName'],
            'address': {
                'streetAddress1': user['address']['streetAddress'],
                'city': user['address']['city'],
                'postalCode': user['address']['postalCode'],
                'country': user['address']['country']
            }
        } for user in users_fixture if user['id'] == staff_id][0]
    associated_images = [{
        'alt': fixture['fields']['alt'],
        'url': urllib.parse.urljoin(settings.MEDIA_URL, fixture['fields']['image']),
    } for fixture in shops_fixture if fixture['model'] == 'product.productimage' and fixture['fields']['product'] == product['pk']]
    # TODO: delete those images from the shops_fixture
    thumbnail = product_thumbnail(
        associated_images) if associated_images else placeholder_product_thumbnail()
    initial_price = get_price(
        variant['fields'], product['fields'])
    conservation = [{
        'mode': item['fields']['conservation_mode'],
        'until': item['fields']['conservation_until']
    } for item in shops_fixture if item['model'] == 'shopozor.product' and item['fields']['product_id'] == product['pk']]
    return product_node(product, variant, new_variant, associated_images, associated_producer, conservation, initial_price, thumbnail)


def postprocess_is_available_flag(edges):
    for edge in edges:
        # an edge is more or less a product
        has_stock = any(variant['stockQuantity'] >
                        0 for variant in edge['node']['variants'])
        for variant in edge['node']['variants']:
            # a variant is available <==> product is visible and has stock
            # a product has stock <==> any of its variant has stock
            variant['isAvailable'] = variant['isAvailable'] and has_stock


def extract_products_from_catalogues(catalogues):
    my_catalogues = deepcopy(catalogues)
    result = []
    for shop in my_catalogues:
        for category in my_catalogues[shop]:
            for edge in my_catalogues[shop][category]['data']['products']['edges']:
                product = {
                    'data': {
                        'product': {}
                    }
                }
                node = edge['node']
                product_id = node['id']
                product_already_exists = [
                    item for item in result if item['data']['product']['id'] == product_id]
                if not product_already_exists:
                    node.pop('productType', None)
                    node.pop('thumbnail', None)
                    product['data']['product'] = node
                    result.append(product)
    return result


def extract_catalogues(catalogues):
    my_catalogues = deepcopy(catalogues)
    for shop in my_catalogues:
        for category in my_catalogues[shop]:
            for edge in my_catalogues[shop][category]['data']['products']['edges']:
                node = edge['node']
                # TODO: remove it if is_published == False
                node.pop('conservation', None)
                node.pop('description', None)
                node.pop('images', None)
                node['pricing']['priceRange']['start'].pop('net', None)
                node['pricing']['priceRange']['start'].pop('tax', None)
                node['pricing']['priceRange']['stop'].pop('net', None)
                node['pricing']['priceRange']['stop'].pop('tax', None)
                node.pop('purchaseCost', None)
                node['producer'].pop('description', None)
                node['producer'].pop('address', None)
                for variant in node['variants']:
                    variant.pop('costPrice', None)
                    variant.pop('pricing', None)
    return my_catalogues
