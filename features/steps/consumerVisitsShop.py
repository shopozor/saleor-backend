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

# TODO: compare the response with a generated graphql response from the fixture data?
@then(u'il obtient pour chaque Shop disponible ses coordonnées géographiques avec sa description générale')
def step_impl(context):
    expected_shops = Shop.objects.all()
    shop_edges_data = context.response['data']['shops']['edges']
    context.test.assertEqual(expected_shops.count(), len(shop_edges_data))

    for edge in shop_edges_data:
        shop_data = edge['node']
        context.test.assertTrue(expected_shops.filter(pk=shop_data['id'], name=shop_data['name'], description=shop_data['description'],
                                                      latitude=shop_data['geocoordinates']['latitude'], longitude=shop_data['geocoordinates']['longitude']).exists())


# TODO: complete data_factory with more data like latitude / longitude, name, description when they are ready
# TODO: instead of trying to get the data from the database, get it from the graphql response fixture!
# TODO: maybe generate the response here based on the fixture database Shops.json
@then(u'il obtient la liste de tous les Produits qui y sont publiés')
def step_impl(context):
    selected_shop = context.selected_shop
    raise NotImplementedError('step not yet implemented')
