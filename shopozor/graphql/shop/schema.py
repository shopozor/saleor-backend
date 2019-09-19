import graphene
from graphene import relay

from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from shopozor.models import Shop


class Geocoordinates(graphene.ObjectType):
    latitude = graphene.Decimal(description="Latitude of the shop.")
    longitude = graphene.Decimal(description="Longitude of the shop.")


class ShopNode(DjangoObjectType):
    geocoordinates = graphene.Field(
        Geocoordinates, description="Return geocoordinates of the shop.")

    class Meta:
        model = Shop
        filter_fields = ['name', 'id']
        interfaces = (graphene.relay.Node, )

    def resolve_geocoordinates(root: Shop, _info):
        return Geocoordinates(latitude=root.latitude, longitude=root.longitude)


class ShopsQueries(graphene.ObjectType):
    shop = relay.Node.Field(ShopNode)
    shops = DjangoFilterConnectionField(ShopNode)
