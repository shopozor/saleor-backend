import os
import json

from collections import defaultdict
from django.conf import settings
from saleor.core.utils.random_data import create_product_types, create_categories, create_attributes, create_attributes_values, create_products, create_product_variants, create_collections
from saleor.core.utils.json_serializer import object_hook
from saleor.product.models import ProductVariant
from shopozor.models import Shop

# TODO: complete with more data like latitude / longitude, name, description
# TODO: refactor this code; we have duplication


class ProductFactory:
    def __init__(self, create_images=True):
        self.PLACEHOLDERS_DIR = settings.SALEOR_PLACEHOLDERS_DIR
        self.CREATE_IMG = create_images
        self.PATH_TO_JSON_DB = settings.PATH_TO_SALEOR_JSON_DB

    def create(self):
        with open(self.PATH_TO_JSON_DB) as f:
            db_items = json.load(f, object_hook=object_hook)
        types = defaultdict(list)
        # Sort db objects by its model
        for item in db_items:
            model = item.pop("model")
            types[model].append(item)

        create_product_types(product_type_data=types["product.producttype"])
        create_categories(
            categories_data=types["product.category"], placeholder_dir=self.PLACEHOLDERS_DIR
        )
        create_attributes(attributes_data=types["product.attribute"])
        create_attributes_values(values_data=types["product.attributevalue"])
        create_products(
            products_data=types["product.product"],
            placeholder_dir=self.PLACEHOLDERS_DIR,
            create_images=self.CREATE_IMG,
        )
        create_product_variants(variants_data=types["product.productvariant"])


class ShopFactory:
    # TODO: it can be that we want to add images to each Shop for description purposes
    # in that case we'd need to add a link to an image to the Shop
    # and also to create a placeholder folder with images
    def __init__(self):
        self.PATH_TO_JSON_DB = settings.PATH_TO_SHOPOZOR_JSON_DB

    def create(self):
        with open(self.PATH_TO_JSON_DB) as f:
            db_items = json.load(f, object_hook=object_hook)
        types = defaultdict(list)
        # Sort db objects by its model
        for item in db_items:
            model = item.pop("model")
            types[model].append(item)

        self.create_shops(shops_data=types["shopozor.shop"])

    def create_shops(self, shops_data):
        for shop_data in shops_data:
            pk = shop_data["pk"]
            defaults = shop_data["fields"]
            product_variants_in_shop = defaults.pop("product_variants")
            shop = Shop.objects.update_or_create(pk=pk, defaults=defaults)[0]
            shop.product_variants.set(ProductVariant.objects.filter(
                pk__in=product_variants_in_shop))
