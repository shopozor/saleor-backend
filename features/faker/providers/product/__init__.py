from django.conf import settings
from faker.providers.lorem.la import Provider as LoremProvider

import os


class Provider(LoremProvider):

    variant_names = (
        '1l', '2l', '2.5l', '5l', '250ml', '500ml', '45cm x 45cm', '55cm x 55cm', 'XS', 'S', 'M', 'L', 'XL', '100g', '200g', '250g', '500g', '1kg'
    )

    def __random_float(self, min, max, nb_digits):
        return round(self.generator.random.uniform(min, max), nb_digits)

    def __random_bool(self):
        return bool(self.generator.random.getrandbits(1))

    def category_image_url(self):
        return os.path.join('categories', 'images', '%s.png' % ''.join(self.random_letters()))

    def description(self):
        return self.text(max_nb_chars=200)

    def has_variants(self):
        return self.__random_bool()

    def is_published(self):
        return self.__random_bool()

    def money_amount(self):
        return {
            '_type': 'Money',
            'amount': str(self.__random_float(0, 100, 2)),
            'currency': settings.DEFAULT_CURRENCY
        }

    def price_override(self):
        return self.money_amount() if self.__random_bool() else None

    def product_image_url(self):
        return os.path.join('products', 'images', '%s.png' % ''.join(self.random_letters()))

    def product_name(self):
        return self.sentence(nb_words=3, variable_nb_words=True)

    def shop(self, pk, latitude, longitude, variant_ids):
        return {
            'model': 'shopozor.shop',
            'pk': pk,
            'fields': {
                'description': self.description(),
                'name': self.sentence(nb_words=5, variable_nb_words=True),
                'latitude': latitude,
                'longitude': longitude,
                'product_variants': variant_ids
            }
        }

    def quantity(self):
        return self.random_int(min=0, max=1000)

    def quantity_allocated(self, quantity):
        return self.random_int(min=0, max=quantity)

    def sku(self):
        return str(self.random_number(digits=9, fix_len=True))

    def variant_name(self):
        return self.word(ext_word_list=self.variant_names)

    def weight(self):
        return self.__random_float(0, 100, 2)
