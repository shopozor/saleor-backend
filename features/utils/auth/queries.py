from features.utils.auth.credentials_checks import check_compulsory_login_credential_arguments
from features.utils.graphql.loader import get_query_from_file
from tests.api.utils import get_graphql_content


def login(client, **kwargs):
    check_compulsory_login_credential_arguments(kwargs)
    query = get_query_from_file('login.graphql')
    response = client.post_graphql(query, kwargs)
    return get_graphql_content(response)
