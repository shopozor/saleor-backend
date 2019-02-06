from shopozor.settings import *
import os.path

FIXTURES_FOLDER = os.path.join('features', 'fixtures')
GRAPHQL_QUERIES_FOLDER = os.path.join(FIXTURES_FOLDER, 'graphql')

INSTALLED_APPS.append('behave_django')
