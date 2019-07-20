from behave import given, then, when
from features.utils.graphql.loader import get_query_from_file
from shopozor.models import Shop
from tests.api.utils import get_graphql_content


def query_shops(client):
    query = get_query_from_file('shops.graphql')
    response = client.post_graphql(query)
    return get_graphql_content(response)


@when(u'Incognito demande quels Shops il peut visiter')
def step_impl(context):
    test_client = context.test.client
    context.response = query_shops(test_client)


@then(u'il obtient pour chaque Shop disponible ses coordonnées géographiques avec sa description générale')
def step_impl(context):
    expected_shops = context.shops
    shop_edges_data = context.response['data']['shops']['edges']
    context.test.assertEqual(expected_shops.count(), len(shop_edges_data))

    for edge in shop_edges_data:
        shop_data = edge['node']
        context.test.assertTrue(expected_shops.filter(name=shop_data['name'], description=shop_data['description'],
                                                      latitude=shop_data['geocoordinates']['latitude'], longitude=shop_data['geocoordinates']['longitude']).exists())
