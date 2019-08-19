from django.conf import settings
from faker import Faker
from features.faker.providers.geo import Provider as ShopozorGeoProvider
from features.faker.providers.product_variant import Provider as ProductVariantProvider
from features.utils.fixtures import json

import os
import unidecode

fake = Faker('fr_CH')
fake.seed('features')

fake.add_provider(ShopozorGeoProvider)
fake.add_provider(ProductVariantProvider)

PATH_TO_SALEOR_FIXTURE = os.path.join(settings.FIXTURE_DIRS[0], 'saleor.json')


class UserFactory:

    def create_email(first_name, last_name):
        domain_name = fake.free_email_domain()
        return unidecode.unidecode('%s.%s@%s' % (first_name, last_name, domain_name))

    def create_consumers(list_size=1):
        result = []
        for _ in range(0, list_size):
            result.append({
                'email': fake.email(),
                'isActive': True
            })
        return result

    def create_producers(list_size=1):
        result = []
        for _ in range(0, list_size):
            first_name = fake.first_name()
            last_name = fake.last_name()
            result.append({
                # get rid of any potential French accent from the first and last name
                'email': UserFactory.create_email(first_name, last_name),
                'isActive': True,
                'isStaff': True,
                'first_name': first_name,
                'last_name': last_name
            })
        return result

    def create_managers(list_size=1):
        result = []
        for _ in range(0, list_size):
            first_name = fake.first_name()
            last_name = fake.last_name()
            result.append({
                # get rid of any potential French accent from the first and last name
                'email': UserFactory.create_email(first_name, last_name),
                'isActive': True,
                'isStaff': True,
                'first_name': first_name,
                'last_name': last_name,
                'permissions': [{
                    'code': 'MANAGE_PRODUCERS'
                }]
            })
        return result

    def create_shops(nb_variants, list_size=1):
        result = []
        products_fixture = json.load(PATH_TO_SALEOR_FIXTURE)
        product_variant_ids = [
            item['pk'] for item in products_fixture if item['model'] == 'product.productvariant']

        for shop_id in range(0, list_size):
            result.append({
                'model': 'shopozor.shop',
                'pk': shop_id,
                'fields': {
                    'description': fake.text(max_nb_chars=200, ext_word_list=None),
                    'name': fake.sentence(nb_words=5, variable_nb_words=True, ext_word_list=None),
                    'latitude': float(fake.local_latitude()),
                    'longitude': float(fake.local_longitude()),
                    'product_variants': fake.variant_ids(product_variant_ids, nb_variants)
                }
            })
        return result
