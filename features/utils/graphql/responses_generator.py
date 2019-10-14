from features.utils.fixtures import json
import features.utils.graphql.responses_generator_helpers as helpers

import abc
import graphene
import os


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
        self.__SHOPS_FIXTURE = helpers.get_shopozor_fixture(fixture_variant)
        super().__init__(os.path.join(output_dir, fixture_variant, 'Consumer'))

    def _produce_data(self):
        return {
            'data': {
                'shops': {
                    'edges': [helpers.shop_node(shop_fixture['pk'], shop_fixture['fields']) for shop_fixture in [shop for shop in self.__SHOPS_FIXTURE if shop['model'] == 'shopozor.shop']]
                }
            }
        }

    def generate(self):
        self._to_json(self._produce_data(), 'Shops.json')


class ShopCategoriesGenerator(ResponsesGenerator):

    def __init__(self, output_dir, fixture_variant):
        self.__SHOPS_FIXTURE = helpers.get_shopozor_fixture(fixture_variant)
        super().__init__(os.path.join(output_dir, fixture_variant, 'Consumer'))

    def _produce_data(self):
        return {
            'data': {
                'categories': {
                    'edges': [helpers.category_node(category['pk'], category['fields']) for category in [item for item in self.__SHOPS_FIXTURE if item['model'] == 'product.category']],
                }
            }
        }

    def generate(self):
        expected_categories = self._produce_data()
        helpers.set_page_info(expected_categories['data']['categories'])
        self._to_json(expected_categories, 'Categories.json')


class ProductListsGenerator(ResponsesGenerator):

    def __init__(self, output_dir, fixture_variant):
        self.__SHOPS_FIXTURE = helpers.get_shopozor_fixture(fixture_variant)
        self.__USERS_FIXTURE = helpers.get_users_fixture(fixture_variant)
        super().__init__(os.path.join(output_dir, fixture_variant, 'Consumer'))

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
                        edge for edge in catalogue_edges if int(graphene.Node.from_global_id(edge['node']['id'])[1]) == product['pk']]

                    shopozor_product = [item['fields'] for item in self.__SHOPS_FIXTURE if item['model']
                                        == 'shopozor.product' and item['fields']['product_id'] == product['pk']][0]

                    new_variant = helpers.variant_node(
                        variant_id, variant['fields'], product['fields'], shopozor_product)

                    if edges_with_product_id:
                        edge = edges_with_product_id[0]
                        helpers.append_variant_to_existing_product(
                            edge['node'], new_variant, variant, product, shopozor_product)
                    else:
                        node = helpers.create_new_product_with_variant(
                            product, variant, new_variant, self.__USERS_FIXTURE, self.__SHOPS_FIXTURE)
                        catalogue_edges.append(node)
                        totalCount += 1
                helpers.set_page_info(
                    product_catalogues[shop['pk']][category]['data']['products'], totalCount)

                helpers.postprocess_is_available_flag(catalogue_edges)
                helpers.postprocess_margins(catalogue_edges)
        return product_catalogues

    def __output_catalogues(self, shop_catalogues):
        for catalogue in shop_catalogues:
            output_dir = os.path.join('Catalogues', 'Shop-%d' % catalogue)
            for category in shop_catalogues[catalogue]:
                output_filename = os.path.join(
                    output_dir, 'Category-%d.json' % category)
                self._to_json(
                    shop_catalogues[catalogue][category], output_filename)

    def __output_product_details(self, product_details):
        for detail in product_details:
            product_id = int(graphene.Node.from_global_id(
                detail['data']['product']['id'])[1])
            output_filename = os.path.join(
                'Products', 'Product-%d.json' % product_id)
            self._to_json(detail, output_filename)

    def generate(self):
        product_catalogues = self._product_data()
        expected_product_details = helpers.extract_products_from_catalogues(
            product_catalogues)
        expected_catalogues = helpers.extract_catalogues(product_catalogues)
        self.__output_catalogues(expected_catalogues)
        self.__output_product_details(expected_product_details)
        # TODO: output unpublished products too
