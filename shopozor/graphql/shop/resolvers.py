import graphene
import graphene_django_optimizer as gql_optimizer

from saleor.product import models as saleorModels


def resolve_categories(info, query, level=None):
    qs = saleorModels.Category.objects.prefetch_related("children")
    if level is not None:
        qs = qs.filter(level=level)
    return gql_optimizer.query(qs, info)
