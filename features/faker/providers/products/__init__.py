import factory
from faker.providers import BaseProvider
import string


class ProductVariantProvider(BaseProvider):

    names = ['1l', '2l', '5l', '250ml', '500ml', '750ml',
             '30cl', '70cl', '100g', '250g', '500g', '1kg']

    def variant_sku(self):
        """
        :example '0PdytfnL89W9K'
        """
        allowed_chars = tuple(string.digits + string.ascii_letters)
        return ''.join(self.random_elements(allowed_chars))

    def variant_name(self):
        """
        :example '250ml'
        """
        return self.random_element(self.names)


factory.Faker.add_provider(ProductVariantProvider)
