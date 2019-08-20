from faker import Faker
from features.faker.providers.geo import Provider as ShopozorGeoProvider
from features.faker.providers.product_variant import Provider as ProductVariantProvider

import os
import unidecode

fake = Faker('fr_CH')
fake.seed('features')

fake.add_provider(ShopozorGeoProvider)
fake.add_provider(ProductVariantProvider)


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

    def create_shops(producer_ids, products, product_variants, list_size=1):
        result = []

        for shop_id in range(0, list_size):
            # TODO
            # 1. choose a few producers
            # 2. choose a few products
            # 3. take all variants associated with each product of step 2
            # n. remove the few producers of step 1 from the original list of producers
            # n. remove the few products of step 2 from the original list of products
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
