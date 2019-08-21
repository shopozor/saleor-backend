from faker.providers.lorem.la import Provider as LoremProvider


class Provider(LoremProvider):

    def weight(self):
        return round(self.generator.random.uniform(0, 100), 2)

    def random_bool(self):
        return bool(self.generator.random.getrandbits(1))

    def has_variants(self):
        return self.random_bool()

    def shop(self, pk, latitude, longitude, variant_ids):
        return {
            'model': 'shopozor.shop',
            'pk': pk,
            'fields': {
                'description': self.text(max_nb_chars=200, ext_word_list=None),
                'name': self.sentence(nb_words=5, variable_nb_words=True, ext_word_list=None),
                'latitude': latitude,
                'longitude': longitude,
                'product_variants': variant_ids
            }
        }
