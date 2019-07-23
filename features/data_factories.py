import factory
from features.faker.providers import product_variant
from saleor.product.models import ProductVariant
from shopozor.models import Shop


class ShopFactory(factory.Factory):
    class Meta:
        model = Shop

    name = factory.Faker('name')
    description = factory.Faker('sentence', nb_words=20)
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')


class ProductVariantFactory(factory.Factory):
    class Meta:
        model = ProductVariant

    sku = factory.Faker('sku')
