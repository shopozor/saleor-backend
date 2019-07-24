import factory
from features.faker.providers import products, price
from saleor.product.models import ProductVariant
from shopozor.models import Shop


class ShopFactory(factory.Factory):
    class Meta:
        model = Shop

    name = factory.Faker('name')
    description = factory.Faker('sentence', nb_words=20)
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')

    # TODO: to link to Products or Producers or whatever, use SubFactory
    # https://factoryboy.readthedocs.io/en/latest/recipes.html#dependent-objects-foreignkey


class ProductVariantFactory(factory.Factory):
    class Meta:
        model = ProductVariant

    sku = factory.Faker('variant_sku')
    name = factory.Faker('variant_name')
    price_override = factory.Faker('money')
    # this currently only takes 'kg' into account
    weight = factory.Faker('weight')
