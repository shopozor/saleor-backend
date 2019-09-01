from django.conf import settings
from prices import Money
from saleor.product.models import Category, Product, ProductType, ProductVariant
from shopozor.models import Shop


def test_shop_catalogues_product():
    category = Category()
    category.save()
    product_type = ProductType()
    product_type.save()
    price = Money(amount=10, currency=settings.DEFAULT_CURRENCY)
    product = Product.objects.create(
        category=category, name='Test product', price=price, product_type=product_type)
    variant = ProductVariant(product=product)
    variant.save()
    assert 0 == variant.shop_set.count()
    shop = Shop()
    shop.save()
    shop.product_variants.add(variant)
    assert 1 == variant.shop_set.count()
