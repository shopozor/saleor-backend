import factory

from shopozor.models import Shop


class ShopFactory(factory.Factory):
    class Meta:
        model = Shop

    name = factory.Faker('name')
    description = factory.Faker('sentence', nb_words=20)
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')
