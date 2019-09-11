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
        os.makedirs(self._OUTPUT_DIR, exist_ok=True)
        json.dump(object, os.path.join(self._OUTPUT_DIR, output_filename))


class ShopListsGenerator(ResponsesGenerator):

    def __init__(self, output_dir, fixture_variant):
        self.__SHOPS_FIXTURE = json.load(os.path.join(
            settings.FIXTURE_DIRS[0], fixture_variant, 'Shopozor.json'))
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
        self.__SHOPS_FIXTURE = json.load(os.path.join(
            settings.FIXTURE_DIRS[0], fixture_variant, 'Shopozor.json'))
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
