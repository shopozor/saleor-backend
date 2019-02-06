from shopozor.settings import *

import json
import os.path

FIXTURES_FOLDER = os.path.join('features', 'fixtures')
GRAPHQL_QUERIES_FOLDER = os.path.join(FIXTURES_FOLDER, 'graphql')

INSTALLED_APPS.append('behave_django')

ACCEPTANCE_TESTING = True

with open(os.path.join(FIXTURES_FOLDER, 'Authentication', 'Credentials', 'Jwt.json')) as file:
    jwt_data = json.load(file)

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=30),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=360),
    'JWT_SECRET_KEY': jwt_data['secret'],
    'JWT_ALGORITHM': jwt_data['algorithm']
}
