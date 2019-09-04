from behave import given, then, when
from features.utils.graphql.loader import get_query_from_file
from saleor.product.models import Category
from shopozor.models import Shop
from tests.api.utils import get_graphql_content


def query_shops(client):
    query = get_query_from_file('shops.graphql')
    response = client.post_graphql(query)
    return get_graphql_content(response)


def query_shop_catalogue(client, shop_id, category_id):
    query = get_query_from_file('shopCatalogue.graphql')
    variables = {
        'shopId': shop_id,
        'categoryId': category_id
    }
    response = client.post_graphql(query, variables)
    return get_graphql_content(response)


def query_categories(client):
    query = get_query_from_file('categories.graphql')
    response = client.post_graphql(query)
    return get_graphql_content(response)


def query_product_details(client, product_id):
    query = get_query_from_file('productDetails.graphql')
    variables = {
        'productId': product_id
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


@when(u'Incognito en visite les stands')
def step_impl(context):
    test_client = context.test.client
    for category_id in Category.objects.all():
        context.response[category_id] = query_shop_catalogue(
            test_client, context.shop_id, category_id)


@when(u'Incognito y inspecte un Produit')
def step_impl(context):
    shop = Shop.objects.get(pk=context.shop_id)
    context.product_id = shop.product_variants[0].id
    test_client = context.test.client
    context.response = query_product_details(test_client, context.product_id)


@then(u'il obtient pour chaque Shop disponible ses coordonnées géographiques avec sa description générale')
def step_impl(context):
    context.test.assertEqual(context.expected_shop_list, context.response)


@then(u'il obtient la liste de tous les Produits qui y sont publiés')
def step_impl(context):
    context.test.assertEqual(
        context.expected_shop_catalogues[context.shop_id], context.response)


@then(u'il en obtient la description détaillée')
def step_impl(context):
    raise NotImplementedError()
