from behave import given, then, when
from django.conf import settings
from features.utils.graphql.loader import get_query_from_file
from saleor.product.models import Category, Product
from shopozor.models import Shop
from tests.api.utils import get_graphql_content

import graphene


def query_shops(client):
    query = get_query_from_file('shops.graphql')
    variables = {
        'first': Shop.objects.count(),
    }
    response = client.post_graphql(query, variables)
    return get_graphql_content(response)


def query_shop_catalogue(client, shop_id, category_id):
    query = get_query_from_file('shopCatalogue.graphql')
    variables = {
        'shopId': graphene.Node.to_global_id("Shop", shop_id),
        'categoryId': graphene.Node.to_global_id("Category", category_id),
        'first': Product.objects.count(),
        'thumbnailSize': settings.PRODUCT_THUMBNAIL_SIZE
    }
    response = client.post_graphql(query, variables)
    return get_graphql_content(response)


def query_categories(client):
    query = get_query_from_file('shopCategories.graphql')
    variables = {
        'first': Category.objects.count(),
        'thumbnailSize': settings.CATEGORY_THUMBNAIL_SIZE
    }
    response = client.post_graphql(query, variables)
    return get_graphql_content(response)


def query_product_details(client, product_id):
    query = get_query_from_file('productDetails.graphql')
    variables = {
        'productId': graphene.Node.to_global_id("Product", product_id)
    }
    response = client.post_graphql(query, variables)
    return get_graphql_content(response)


@given(u'le Shop de son choix')
def step_impl(context):
    context.shop_id = 1


@when(u'Incognito demande quels Shops il peut visiter')
def step_impl(context):
    test_client = context.test.client
    context.response = query_shops(test_client)


@when(u'Incognito se renseigne sur les différents Rayons disponibles dans le Shopozor')
def step_impl(context):
    test_client = context.test.client
    context.response = query_categories(test_client)


@when(u'Incognito en visite les Rayons')
def step_impl(context):
    test_client = context.test.client
    for category in Category.objects.all():
        context.response[category.id] = query_shop_catalogue(
            test_client, context.shop_id, category.id)


@when(u'Incognito y inspecte un Produit')
def step_impl(context):
    shop = Shop.objects.get(pk=context.shop_id)
    context.product_id = shop.product_variants.first().product.id
    test_client = context.test.client
    context.response = query_product_details(test_client, context.product_id)


@then(u'il obtient pour chaque Shop disponible ses coordonnées géographiques avec sa description générale')
def step_impl(context):
    context.test.assertEqual(context.expected_shop_list, context.response)


@then(u'il en obtient la liste')
def step_impl(context):
    context.test.assertEqual(context.expected_categories, context.response)


@then(u'il obtient la liste de tous les Produits qui y sont publiés')
def step_impl(context):
    context.test.assertEqual(
        context.expected_shop_catalogues[context.shop_id], context.response)


@then(u'il en obtient la description détaillée')
def step_impl(context):
    expected_details = context.expected_product_details[context.product_id]
    context.test.assertEqual(expected_details, context.response)


def details_show_product_purchase_cost(product_details):
    return 'purchaseCost' in product_details


def details_show_margin_on_product(product_details):
    return all(price_type in product_details['pricing']['priceRange'][price_range] for price_range in ('start', 'stop') for price_type in ('gross', 'net', 'tax'))


def details_show_variants_cost_prices(product_details):
    return all('costPrice' in variant for variant in product_details['variants'])


def details_show_margin_on_variants(product_details):
    return all(price_type in variant['pricing']['price'] for variant in product_details['variants'] for price_type in ('gross', 'net', 'tax'))


@then(u'une indication claire de la marge que s\'en fait le Shopozor')
def step_impl(context):
    details = context.response['data']['product']
    context.test.assertTrue(details_show_product_purchase_cost(details))
    context.test.assertTrue(details_show_margin_on_product(details))
    context.test.assertTrue(details_show_variants_cost_prices(details))
    context.test.assertTrue(details_show_margin_on_variants(details))
