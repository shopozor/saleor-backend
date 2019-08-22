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
    print('nbr of shops = ', Shop.objects.count())
    test_client = context.test.client
    context.response = query_shops(test_client)
    raise NotImplementedError('step not implemented')


@when(u'Incognito visite un Shop')
def step_impl(context):
    shop = Shop.objects.first()
    context.current_shop = shop
    test_client = context.test.client
    context.response = query_shop_catalogue(test_client, shop.id)


@then(u'il obtient pour chaque Shop disponible ses coordonnées géographiques avec sa description générale')
def step_impl(context):
    context.test.assertEqual(context.expected_shop_list, context.response)


# TODO: complete data_factory with more data like latitude / longitude, name, description when they are ready
# TODO: instead of trying to get the data from the database, get it from the graphql response fixture!
# TODO: maybe generate the response here based on the fixture database Shops.json
@then(u'il obtient la liste de tous les Produits qui y sont publiés')
def step_impl(context):
    current_shop = context.current_shop
    raise NotImplementedError('step not yet implemented')
