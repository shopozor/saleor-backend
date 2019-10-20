import os
import graphene

from graphene_django.types import DjangoObjectType

from saleor.graphql.core.connection import CountableDjangoObjectType
from saleor.graphql.core.fields import FilterInputConnectionField, PrefetchingConnectionField
from saleor.graphql.core.types import common

from saleor.product import models as saleorModels
from saleor.product.templatetags.product_images import get_thumbnail_size

from shopozor import models
from .resolvers import resolve_categories


class Geocoordinates(graphene.ObjectType):
    latitude = graphene.Float(description="Latitude of the shop.")
    longitude = graphene.Float(description="Longitude of the shop.")


class Shop(CountableDjangoObjectType):
    geocoordinates = graphene.Field(
        Geocoordinates, description="Return geocoordinates of the shop.")

    class Meta:
        description = "A shop of the shopozor"
        only_fields = [
            "id",
            "name",
            "description",
            "geocoordinates"
        ]
        interfaces = [graphene.relay.Node]
        model = models.Shop

    def resolve_geocoordinates(root: models.Shop, _info):
        return Geocoordinates(latitude=root.latitude, longitude=root.longitude)


class Category(CountableDjangoObjectType):
    url = graphene.String(description="The storefront's URL for the category.")
    background_image = graphene.Field(
        common.Image, size=graphene.Int(description="Size of the image")
    )

    class Meta:
        description = "Represents a single category of products."
        only_fields = [
            "id",
            "name",
            "description",
            "background_image"
        ]
        interfaces = [graphene.relay.Node]
        model = saleorModels.Category

    @staticmethod
    def resolve_background_image(root: saleorModels.Category, info, size=None, **_kwargs):
        if root.background_image:
            if size:
                used_size = get_thumbnail_size(
                    size, "thumbnail", "background_images")
                filename, file_extension = os.path.splitext(
                    root.background_image.url)
                url = filename + "-thumbnail-" + \
                    str(used_size) + file_extension
                return common.Image(url, root.background_image_alt)
            return root.background_image


class ShopsQueries(graphene.ObjectType):
    shop = graphene.Field(
        Shop,
        id=graphene.Argument(graphene.ID, required=True),
        description="Lookup a shop by ID.",
    )

    shops = FilterInputConnectionField(
        Shop,
        description="List of shops.",
    )

    category = graphene.Field(
        Category,
        id=graphene.Argument(graphene.ID, required=True),
        description="Lookup a category by ID.",
    )

    categories = PrefetchingConnectionField(
        Category,
        level=graphene.Argument(graphene.Int),
        description="List of the shop's categories.",
    )

    def resolve_shop(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, models.Shop)

    def resolve_shops(self, info, **kwargs):
        return models.Shop.objects.all()

    def resolve_category(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, saleorModels.Category)

    def resolve_categories(self, info, level=None, query=None, **_kwargs):
        return resolve_categories(info, level=level, query=query)
