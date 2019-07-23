from behave import given, then, when
from features.utils.graphql.loader import get_query_from_file
from shopozor.models import Shop
from tests.api.utils import get_graphql_content


def query_shops(client):
    query = get_query_from_file('shops.graphql')
    response = client.post_graphql(query)
    return get_graphql_content(response)


def query_shop_catalogue(client, shop_id):
    query = get_query_from_file('shopCatalogue.graphql')
    variables = {
        'shopId': shop_id
    }
    response = client.post_graphql(query, variables)
    return get_graphql_content(response)


@when(u'Incognito demande quels Shops il peut visiter')
def step_impl(context):
    test_client = context.test.client
    context.response = query_shops(test_client)


@when(u'Incognito visite un Shop')
def step_impl(context):
    shop = Shop.objects.first()
    context.selected_shop = shop
    test_client = context.test.client
    context.response = query_shop_catalogue(test_client, shop.id)


@then(u'il obtient pour chaque Shop disponible ses coordonnées géographiques avec sa description générale')
def step_impl(context):
    expected_shops = context.shops
    shop_edges_data = context.response['data']['shops']['edges']
    context.test.assertEqual(expected_shops.count(), len(shop_edges_data))

    for edge in shop_edges_data:
        shop_data = edge['node']
        context.test.assertTrue(expected_shops.filter(pk=shop_data['id'], name=shop_data['name'], description=shop_data['description'],
                                                      latitude=shop_data['geocoordinates']['latitude'], longitude=shop_data['geocoordinates']['longitude']).exists())


@then(u'il obtient la liste de tous les Produits qui y sont publiés')
def step_impl(context):
    # 0. prepare product fixtures to allow for this step!
    # 1. get selected shop from context
    # 2. get products from selected shop
    # 3. compare products' properties with those received in the response (id, name, variants, category, productType)
    raise NotImplementedError('step not yet implemented')
