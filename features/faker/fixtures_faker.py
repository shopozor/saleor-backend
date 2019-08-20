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

    def create_shops(producers, products, product_variants, list_size=1):
        result = []

        max_nb_producers_per_shop = 10
        for shop_id in range(0, list_size):
            # TODO
            # 1. choose a few producers
            # producer_ids = fake.producer_ids(max_nb_producers_per_shop)
            nb_producers = fake.random.randint(1, max_nb_producers_per_shop)
            shop_producers = fake.random_elements(
                elements=producers, length=nb_producers, unique=True)
            # 2. for each producer:

            # 2.1 choose a few products
            # 2.2 associate producers with products
            # 3 take all variants associated with each product of step 2
            # 4. remove the few producers of step 1 from the original list of producers
            # 5. remove the few products of step 2 from the original list of products

            result.append({
                'model': 'shopozor.shop',
                'pk': shop_id,
                'fields': {
                    'description': fake.text(max_nb_chars=200, ext_word_list=None),
                    'name': fake.sentence(nb_words=5, variable_nb_words=True, ext_word_list=None),
                    'latitude': float(fake.local_latitude()),
                    'longitude': float(fake.local_longitude()),
                    # 'product_variants': fake.variant_ids(product_variant_ids, nb_variants)
                    'product_variants': []
                }
            })
        return result

# TODO: generate productstaff model instances before generating the shops!
