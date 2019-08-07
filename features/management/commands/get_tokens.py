import os

from django.contrib.auth.models import AnonymousUser
from django.core.management.base import BaseCommand
from features.utils.fixtures.loader import get_data_from_json_fixture
from features.utils.graphql.loader import get_query_from_file
from tests.api.conftest import ApiClient
from tests.api.utils import get_graphql_content


def login_query():
    queryfile = 'login.graphql'
    return get_query_from_file(queryfile)


def get_user_tokens():
    query = login_query()
    client = ApiClient(user=AnonymousUser())
    result = {}
    for persona in 'Consommateurs', 'Producteurs', 'Responsables', 'Rex', 'Softozor':
        user_data = get_data_from_json_fixture(os.path.join(
            'Authentication', 'Credentials', persona + '.json'))
        if isinstance(user_data, list):
            user = user_data[0]
        else:
            user = user_data
        variables = dict(email=user['email'],
                         password=user['password'])
        response = get_graphql_content(client.post_graphql(query, variables))
        result[persona] = response['data']['login']['token']
    return result


class Command(BaseCommand):
    help = 'Logs all Personas (Consommateur, Producteur, Responsable, Rex, Softozor) in and print their token.'

    def handle(self, *args, **options):
        user_tokens = get_user_tokens()
        print(user_tokens)
