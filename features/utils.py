from features.settings import GRAPHQL_QUERIES_FOLDER


def get_query_from_file(filename):
    path_to_query = '/'.join([GRAPHQL_QUERIES_FOLDER, filename])
    with open(path_to_query, 'r') as myfile:
        return myfile.read().replace('\n', '')

