# coding=utf-8
from __future__ import unicode_literals

import factory
from faker.providers import BaseProvider, date_time

import string

localized = True


class Provider(BaseProvider):

    def sku(self):
        """
        :example '0PdytfnL89W9K'
        """
        allowed_chars = tuple(string.digits + string.ascii_letters)
        return ''.join(self.random_elements(allowed_chars))


factory.Faker.add_provider(Provider)
