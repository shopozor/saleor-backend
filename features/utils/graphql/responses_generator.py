from copy import deepcopy
from django.conf import settings
from features.utils.fixtures import json

import abc
import graphene
import os
import urllib.parse


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


class ResponsesGenerator():

    __metaclass__ = abc.ABCMeta

    def __init__(self, output_dir):
        self._OUTPUT_DIR = output_dir

    @abc.abstractmethod
    def _produce_data(self):
        pass

    @abc.abstractmethod
    def generate(self):
        pass

    def _to_json(self, object, output_filename):
        fullpath = os.path.join(self._OUTPUT_DIR, output_filename)
        output_dir = os.path.split(fullpath)[0]
        os.makedirs(output_dir, exist_ok=True)
        json.dump(object, fullpath)


class ShopListsGenerator(ResponsesGenerator):

    def __init__(self, output_dir, fixture_variant):
        self.__SHOPS_FIXTURE = get_shopozor_fixture(fixture_variant)
        super().__init__(os.path.join(output_dir, fixture_variant, 'Consumer'))

    def __shop_node(self, shop_id, shop_fields):
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

    def _produce_data(self):
        return {
            'data': {
                'shops': {
                    'edges': [self.__shop_node(shop_fixture['pk'], shop_fixture['fields']) for shop_fixture in [shop for shop in self.__SHOPS_FIXTURE if shop['model'] == 'shopozor.shop']]
                }
            }
        }

    def generate(self):
        self._to_json(self._produce_data(), 'Shops.json')


class ShopCategoriesGenerator(ResponsesGenerator):

    def __init__(self, output_dir, fixture_variant):
        self.__SHOPS_FIXTURE = get_shopozor_fixture(fixture_variant)
        super().__init__(os.path.join(output_dir, fixture_variant, 'Consumer'))

    def __category_node(self, category_id, category_fields):
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

    def _produce_data(self):
        return {
            'data': {
                'categories': {
                    'edges': [self.__category_node(category['pk'], category['fields']) for category in [item for item in self.__SHOPS_FIXTURE if item['model'] == 'product.category']],
                }
            }
        }

    def generate(self):
        expected_categories = self._produce_data()
        set_page_info(expected_categories['data']['categories'])
        self._to_json(expected_categories, 'Categories.json')


class ProductListsGenerator(ResponsesGenerator):

    def __init__(self, output_dir, fixture_variant):
        self.__SHOPS_FIXTURE = get_shopozor_fixture(fixture_variant)
        self.__USERS_FIXTURE = get_users_fixture(fixture_variant)
        super().__init__(os.path.join(output_dir, fixture_variant, 'Consumer'))

    # TODO: look for methods that don't need 'self'!
    def __money_amount(self, price_fields, amount=None):
        return {
            'amount': amount if amount is not None else price_fields['amount'],
            'currency': price_fields['currency']
        }

    def __get_price(self, variant_fields, product_fields):
        # This method is perfectly fine as long as we don't incorporate taxes
        # When we take taxes into account, we'll need to adapt this method
        # This will document how the taxes are taken into account
        price = {}
        if 'price_override' in variant_fields and variant_fields['price_override'] is not None:
            price = {
                'gross': self.__money_amount(variant_fields['price_override']),
                'net': self.__money_amount(variant_fields['price_override']),
                'tax': self.__money_amount(variant_fields['price_override'], amount=0)
            }
        else:
            price = {
                'gross': self.__money_amount(product_fields['price']),
                'net': self.__money_amount(product_fields['price']),
                'tax': self.__money_amount(product_fields['price'], amount=0)
            }
        return price

    def __create_new_variant(self, variant_id, variant_fields, product_fields):
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
                'price': self.__get_price(variant_fields, product_fields)
            }
        }

    def __price_range(self, start, stop):
        return {
            'priceRange': {
                'start': start,
                'stop': stop
            }
        }

    def __update_product_price_range(self, product, variant, node):
        variant_price = self.__get_price(variant['fields'], product['fields'])
        current_start = node['pricing']['priceRange']['start']
        current_stop = node['pricing']['priceRange']['stop']
        if variant_price['gross']['amount'] < current_start['gross']['amount']:
            return self.__price_range(variant_price, current_stop)
        elif variant_price['gross']['amount'] > current_stop['gross']['amount']:
            return self.__price_range(current_start, variant_price)
        else:
            return self.__price_range(current_start, current_stop)

    def __update_product_purchase_cost(self, variant, node):
        variant_cost = self.__money_amount(variant['fields']['cost_price'])
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

    def __append_variant_to_existing_product(self, node, new_variant, variant, product):
        node['variants'].append(new_variant)
        node['pricing'] = self.__update_product_price_range(
            product, variant, node)
        node['purchaseCost'] = self.__update_product_purchase_cost(
            variant, node)

    def __create_placeholder_product_thumbnail(self):
        return {
            'alt': None,
            'url': urllib.parse.urljoin(settings.STATIC_URL, 'images/placeholder%dx%d.png' % (settings.PRODUCT_THUMBNAIL_SIZE, settings.PRODUCT_THUMBNAIL_SIZE))
        }

    def __create_product_thumbnail(self, associated_images):
        return {
            'alt': associated_images[0]['alt'],
            'url': urllib.parse.urljoin(settings.MEDIA_URL, '__sized__/%s-thumbnail-%dx%d.%s' % (associated_images[0]['url'].split('.')[0], settings.PRODUCT_THUMBNAIL_SIZE, settings.PRODUCT_THUMBNAIL_SIZE, associated_images[0]['url'].split('.')[1]))
        }

    def __create_product(self, product, variant, new_variant, associated_images, associated_producer, conservation, initial_price, thumbnail):
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

    def __create_new_product_with_variant(self, product, variant, new_variant, users_fixture, shops_fixture):
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
        thumbnail = self.__create_product_thumbnail(
            associated_images) if associated_images else self.__create_placeholder_product_thumbnail()
        initial_price = self.__get_price(
            variant['fields'], product['fields'])
        conservation = [{
            'mode': item['fields']['conservation_mode'],
            'until': item['fields']['conservation_until']
        } for item in shops_fixture if item['model'] == 'shopozor.product' and item['fields']['product_id'] == product['pk']]
        return self.__create_product(product, variant, new_variant, associated_images, associated_producer, conservation, initial_price, thumbnail)

    def __postprocess_is_available_flag(self, edges):
        for edge in edges:
            # an edge is more or less a product
            has_stock = any(variant['stockQuantity'] >
                            0 for variant in edge['node']['variants'])
            for variant in edge['node']['variants']:
                # a variant is available <==> product is visible and has stock
                # a product has stock <==> any of its variant has stock
                variant['isAvailable'] = variant['isAvailable'] and has_stock

    def _product_data(self):
        product_catalogues = {}
        for shop in [shop for shop in self.__SHOPS_FIXTURE if shop['model'] == 'shopozor.shop']:
            product_catalogues[shop['pk']] = {}
            for category in [item['pk'] for item in self.__SHOPS_FIXTURE if item['model'] == 'product.category']:
                product_catalogues[shop['pk']][category] = {
                    'data': {
                        'products': {
                            'edges': []
                        }
                    }
                }
                totalCount = 0
                catalogue_edges = product_catalogues[shop['pk']
                                                     ][category]['data']['products']['edges']
                for variant_id in shop['fields']['product_variants']:
                    variant = [entry for entry in self.__SHOPS_FIXTURE if entry['model']
                               == 'product.productvariant' and entry['pk'] == variant_id][0]
                    # TODO: why isn't this working: shops_fixture.remove(variant)?
                    product_in_category = [entry for entry in self.__SHOPS_FIXTURE if entry['model'] ==
                                           'product.product' and entry['pk'] == variant['fields']['product'] and entry['fields']['category'] == category]
                    if len(product_in_category) == 0:
                        continue
                    product = product_in_category[0]
                    is_published = product['fields']['is_published']
                    # TODO: do the job even if the product isn't published; only increment totalCount if is_published == True
                    if not is_published:
                        continue
                    edges_with_product_id = [
                        edge for edge in catalogue_edges if edge['node']['id'] == product['pk']]

                    new_variant = self.__create_new_variant(
                        variant_id, variant['fields'], product['fields'])

                    if edges_with_product_id:
                        edge = edges_with_product_id[0]
                        self.__append_variant_to_existing_product(
                            edge['node'], new_variant, variant, product)
                    else:
                        node = self.__create_new_product_with_variant(
                            product, variant, new_variant, self.__USERS_FIXTURE, self.__SHOPS_FIXTURE)
                        catalogue_edges.append(node)
                        totalCount += 1
                set_page_info(
                    product_catalogues[shop['pk']][category]['data']['products'], totalCount)

        self.__postprocess_is_available_flag(catalogue_edges)
        return product_catalogues

    def extract_products_from_catalogues(self, catalogues):
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

    def extract_catalogues(self, catalogues):
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

    def output_catalogues(self, shop_catalogues):
        for catalogue in shop_catalogues:
            output_dir = os.path.join('Catalogues', 'Shop-%d' % catalogue)
            for category in shop_catalogues[catalogue]:
                output_filename = os.path.join(
                    output_dir, 'Category-%d.json' % category)
                self._to_json(
                    shop_catalogues[catalogue][category], output_filename)

    def output_product_details(self, product_details):
        for detail in product_details:
            product_id = int(graphene.Node.from_global_id(
                detail['data']['product']['id'])[1])
            output_filename = os.path.join(
                'Products', 'Product-%d.json' % product_id)
            self._to_json(detail, output_filename)

    def generate(self):
        product_catalogues = self._product_data()
        expected_product_details = self.extract_products_from_catalogues(
            product_catalogues)
        expected_catalogues = self.extract_catalogues(product_catalogues)
        self.output_catalogues(expected_catalogues)
        self.output_product_details(expected_product_details)
        # TODO: output unpublished products too
