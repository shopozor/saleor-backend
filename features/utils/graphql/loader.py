import os.path

from django.conf import settings


def get_query_from_file(filename):
    path_to_query = os.path.join(settings.GRAPHQL_CALLS_FOLDER, filename)
    with open(path_to_query, 'r') as myfile:
        return myfile.read().replace('\n', '')