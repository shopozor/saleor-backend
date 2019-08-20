from faker import Faker
from features.faker.providers.geo import Provider as ShopozorGeoProvider
from features.faker.providers.product import Provider as ProductProvider

import os
import unidecode

fake = Faker('fr_CH')
fake.seed('features')

fake.add_provider(ShopozorGeoProvider)
fake.add_provider(ProductProvider)

# TODO: change this class' name


class UserFactory:

    def create_email(first_name, last_name):
        domain_name = fake.free_email_domain()
        return unidecode.unidecode('%s.%s@%s' % (first_name, last_name, domain_name))

    def create_consumers(start_index, list_size=1):
        result = []
        for id in range(0, list_size):
            result.append({
                'id': start_index + id,
                'email': fake.email(),
                'isActive': True,
                'isStaff': False,
                'isSuperUser': False,
                'permissions': []
            })
        return result

    def create_producers(start_index, list_size=1):
        result = []
        for id in range(0, list_size):
            first_name = fake.first_name()
            last_name = fake.last_name()
            result.append({
                'id': start_index + id,
                # get rid of any potential French accent from the first and last name
                'email': UserFactory.create_email(first_name, last_name),
                'isActive': True,
                'isStaff': True,
                'isSuperUser': False,
                'first_name': first_name,
                'last_name': last_name,
                'permissions': []
            })
        return result

    def create_managers(start_index, list_size=1):
        result = []
        for id in range(0, list_size):
            first_name = fake.first_name()
            last_name = fake.last_name()
            result.append({
                'id': start_index + id,
                # get rid of any potential French accent from the first and last name
                'email': UserFactory.create_email(first_name, last_name),
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

    def create_rex(start_index):
        return {
            'id': start_index,
            'email': 'rex@%s' % fake.free_email_domain(),
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

    def create_softozor(start_index):
        return {
            'id': start_index,
            'email': 'softozor@%s' % fake.free_email_domain(),
            'isActive': True,
            'isStaff': True,
            'isSuperUser': True,
            'permissions': []
        }

    def create_staff(producers):
        offset = producers[0]['id']
        return [{
            'fields': {
                'user_id': user['id']
            },
            'model': 'shopozor.staff',
            'pk': user['id'] - offset + 1
        } for user in producers]

    def create_productstaff(producers, products):
        product_ids = [product['pk'] for product in products]
        max_nb_products_per_producer = 10
        result = []
        productstaff_pk = 1
        for producer in producers:
            nb_products = fake.random.randint(0, max_nb_products_per_producer)
            try:
                producer_product_ids = fake.random_elements(
                    elements=product_ids, length=nb_products, unique=True)
            except ValueError:
                print('Producer %s %s cannot have products assigned as there are no products anymore' % (
                    producer['first_name'], producer['last_name']))
            for producer_product_id in producer_product_ids:
                result.append({
                    "fields": {
                        "product_id": producer_product_id,
                        "staff_id": producer['id']
                    },
                    "model": "shopozor.productstaff",
                    "pk": productstaff_pk
                })
                productstaff_pk += 1
            product_ids = [
                id for id in product_ids if id not in producer_product_ids]
        return result

    def create_shops(producers, productstaff, product_variants, list_size=1):
        result = []

        producer_ids = [producer['id'] for producer in producers]

        max_nb_producers_per_shop = 10
        for shop_id in range(0, list_size):
            nb_producers = fake.random.randint(0, max_nb_producers_per_shop)
            # 1. get a few producer_ids
            try:
                shop_producer_ids = fake.random_elements(
                    elements=producer_ids, length=nb_producers, unique=True)
            except ValueError:
                print(
                    'Shop %d cannot have producers assigned as there are no producers anymore' % shop_id)
            # 2. get the corresponding product_ids from the productstaff
            shop_product_ids = [item['fields']['product_id'] for item in productstaff if item['model']
                                == 'shopozor.productstaff' and item['fields']['staff_id'] in shop_producer_ids]
            # 3. get the variant_ids of all product_ids from the product_variants list
            variant_ids = [variant['pk']
                           for variant in product_variants if variant['fields']['product'] in shop_product_ids]
            # 4. remove the selected producer_ids from the original producer_ids list
            producer_ids = [
                id for id in producer_ids if id not in shop_product_ids]

            result.append({
                'model': 'shopozor.shop',
                'pk': shop_id + 1,
                'fields': {
                    'description': fake.text(max_nb_chars=200, ext_word_list=None),
                    'name': fake.sentence(nb_words=5, variable_nb_words=True, ext_word_list=None),
                    'latitude': float(fake.local_latitude()),
                    'longitude': float(fake.local_longitude()),
                    'product_variants': variant_ids
                }
            })
        return result
