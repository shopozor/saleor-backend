from faker.providers.lorem.la import Provider as LoremProvider


class Provider(LoremProvider):

    def __random_float(self, min, max, nb_digits):
        return round(self.generator.random.uniform(min, max), nb_digits)

    def weight(self):
        return self.__random_float(0, 100, 2)

    def money_amount(self):
        return str(self.__random_float(0, 100, 2))

    def __random_bool(self):
        return bool(self.generator.random.getrandbits(1))

    def has_variants(self):
        return self.__random_bool()

    def is_published(self):
        return self.__random_bool()

    def description(self):
        return self.text(max_nb_chars=200)

    def product_name(self):
        return self.words()

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
