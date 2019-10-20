from shopozor import models

from saleor.graphql.core.connection import CountableDjangoObjectType

import graphene


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
