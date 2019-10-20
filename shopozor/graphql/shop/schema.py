from .types import Shop, Category
from .resolvers import resolve_categories

from shopozor import models

from saleor.graphql.core.fields import FilterInputConnectionField, PrefetchingConnectionField
from saleor.product import models as saleorModels

import graphene


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
