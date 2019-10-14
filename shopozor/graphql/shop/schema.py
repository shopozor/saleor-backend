import graphene

from graphene_django.types import DjangoObjectType

from saleor.graphql.core.connection import CountableDjangoObjectType
from saleor.graphql.core.fields import FilterInputConnectionField

from shopozor import models


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

    def resolve_shop(self, info, id):
        return graphene.Node.get_node_from_global_id(info, id, models.Shop)

    def resolve_shops(self, info, **kwargs):
        return models.Shop.objects.all()
