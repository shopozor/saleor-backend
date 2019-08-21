from faker import Faker
from features.faker.providers.geo import Provider as ShopozorGeoProvider

import os
import unidecode


class FakeDataFactory:

    def __init__(self):
        self.__fake = Faker('fr_CH')
        self.__fake.seed('features')
        self.__fake.add_provider(ShopozorGeoProvider)

    def create_email(self, first_name, last_name):
        domain_name = self.__fake.free_email_domain()
        return unidecode.unidecode('%s.%s@%s' % (first_name, last_name, domain_name))

    def create_consumers(self, start_index, list_size=1):
        result = []
        for id in range(0, list_size):
            result.append({
                'id': start_index + id,
                'email': self.__fake.email(),
                'isActive': True,
                'isStaff': False,
                'isSuperUser': False,
                'permissions': []
            })
        return result

    def create_producers(self, start_index, list_size=1):
        result = []
        for id in range(0, list_size):
            first_name = self.__fake.first_name()
            last_name = self.__fake.last_name()
            result.append({
                'id': start_index + id,
                # get rid of any potential French accent from the first and last name
                'email': self.create_email(first_name, last_name),
                'isActive': True,
                'isStaff': True,
                'isSuperUser': False,
                'first_name': first_name,
                'last_name': last_name,
                'permissions': []
            })
        return result

    def create_managers(self, start_index, list_size=1):
        result = []
        for id in range(0, list_size):
            first_name = self.__fake.first_name()
            last_name = self.__fake.last_name()
            result.append({
                'id': start_index + id,
                # get rid of any potential French accent from the first and last name
                'email': self.create_email(first_name, last_name),
                'isActive': True,
                'isStaff': True,
                'isSuperUser': False,
                'first_name': first_name,
                'last_name': last_name,
                'permissions': [{
                    'code': 'MANAGE_PRODUCERS'
                }]
            })
        return result

    def create_rex(self, start_index):
        return {
            'id': start_index,
            'email': 'rex@%s' % self.__fake.free_email_domain(),
            'isActive': True,
            'isStaff': True,
            'isSuperUser': False,
            'permissions': [
                {
                    'code': 'MANAGE_STAFF'
                },
                {
                    'code': 'MANAGE_USERS'
                },
                {
                    'code': 'MANAGE_PRODUCERS'
                },
                {
                    'code': 'MANAGE_MANAGERS'
                }
            ]
        }

    def create_softozor(self, start_index):
        return {
            'id': start_index,
            'email': 'softozor@%s' % self.__fake.free_email_domain(),
            'isActive': True,
            'isStaff': True,
            'isSuperUser': True,
            'permissions': []
        }

    def __staff(self, pk, user_id):
        return {
            'fields': {
                'user_id': user_id
            },
            'model': 'shopozor.staff',
            'pk': pk
        }

    def create_staff(self, producers):
        offset = producers[0]['id']
        return [self.__staff(user['id'] - offset + 1, user['id']) for user in producers]

    def __try_to_get_random_elements(self, elements, length):
        try:
            return self.__fake.random_elements(
                elements=elements, length=length, unique=True)
        except ValueError:
            return []

    def __productstaff(self, pk, product_id, producer_id):
        return {
            "fields": {
                "product_id": product_id,
                "staff_id": producer_id
            },
            "model": "shopozor.productstaff",
            "pk": pk
        }

    def create_productstaff(self, producers, products):
        product_ids = [product['pk'] for product in products]
        max_nb_products_per_producer = 10
        result = []
        productstaff_pk = 1
        for producer in producers:
            nb_products = self.__fake.random.randint(
                0, max_nb_products_per_producer)
            producer_product_ids = self.__try_to_get_random_elements(
                product_ids, nb_products)
            for producer_product_id in producer_product_ids:
                result.append(self.__productstaff(
                    productstaff_pk, producer_product_id, producer['id']))
                productstaff_pk += 1
            product_ids = [
                id for id in product_ids if id not in producer_product_ids]
        return result

    def __shop(self, pk, variant_ids):
        return {
            'model': 'shopozor.shop',
            'pk': pk,
            'fields': {
                'description': self.__fake.text(max_nb_chars=200, ext_word_list=None),
                'name': self.__fake.sentence(nb_words=5, variable_nb_words=True, ext_word_list=None),
                'latitude': float(self.__fake.local_latitude()),
                'longitude': float(self.__fake.local_longitude()),
                'product_variants': variant_ids
            }
        }

    def create_shops(self, producers, productstaff, product_variants, list_size=1):
        result = []

        producer_ids = [producer['id'] for producer in producers]

        max_nb_producers_per_shop = 10
        for shop_id in range(0, list_size):
            nb_producers = self.__fake.random.randint(
                0, max_nb_producers_per_shop)
            shop_producer_ids = self.__try_to_get_random_elements(
                producer_ids, nb_producers)
            shop_product_ids = [item['fields']['product_id'] for item in productstaff if item['model']
                                == 'shopozor.productstaff' and item['fields']['staff_id'] in shop_producer_ids]
            variant_ids = [variant['pk']
                           for variant in product_variants if variant['fields']['product'] in shop_product_ids]
            producer_ids = [
                id for id in producer_ids if id not in shop_producer_ids]
            result.append(self.__shop(shop_id + 1, variant_ids))

        return result

#   {
#     "fields": {
#       "attributes": "{\"15\": \"46\", \"21\": \"68\"}",
#       "category": 8,
#       "charge_taxes": true,
#       "description": "Find your sea legs and then lose the power to use them with extra strong seaman\u2019s lager. Don\u2019t drink and sail, me hearties!",
#       "description_json": {
#         "blocks": [
#           {
#             "data": {},
#             "depth": 0,
#             "entityRanges": [],
#             "inlineStyleRanges": [],
#             "key": "",
#             "text": "Find your sea legs and then lose the power to use them with extra strong seaman\u2019s lager. Don\u2019t drink and sail, me hearties!",
#             "type": "unstyled"
#           }
#         ],
#         "entityMap": {}
#       },
#       "is_published": true,
#       "meta": {
#         "taxes": {
#           "vatlayer": {
#             "code": "standard",
#             "description": ""
#           }
#         }
#       },
#       "name": "Seaman Lager",
#       "price": {
#         "_type": "Money",
#         "amount": "3.00",
#         "currency": "CHF"
#       },
#       "product_type": 11,
#       "publication_date": null,
#       "seo_description": "Find your sea legs and then lose the power to use them with extra strong seaman\u2019s lager. Don\u2019t drink and sail, me hearties!",
#       "seo_title": "",
#       "updated_at": "2019-03-06T12:47:38.530Z",
#       "weight": 1.0
#     },
#     "model": "product.product",
#     "pk": 83
#   }
