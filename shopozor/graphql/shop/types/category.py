from saleor.graphql.core.connection import CountableDjangoObjectType
from saleor.graphql.core.types import common
from saleor.product import models as saleorModels
from saleor.product.templatetags.product_images import get_thumbnail_size

import graphene
import os


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
