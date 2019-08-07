from shopozor.settings import *
from datetime import timedelta
import json
from os import environ
import os.path

SALEOR_PROJECT_ROOT = PROJECT_ROOT
PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

PATH_TO_SALEOR_JSON_DB = os.path.join(
    SALEOR_PROJECT_ROOT, "saleor", "static", "populatedb_data.json")
SALEOR_PLACEHOLDERS_DIR = os.path.join(
    SALEOR_PROJECT_ROOT, "saleor", "static", "placeholders")
PATH_TO_SHOPOZOR_JSON_DB = os.path.join(
    PROJECT_ROOT, 'features', 'fixtures', 'Shops.json')

GRAPHQL_RESPONSES_FOLDER = os.path.join('features', 'graphql', 'responses')
GRAPHQL_CALLS_FOLDER = os.path.join('features', 'graphql', 'calls')

INSTALLED_APPS.append('behave_django')
INSTALLED_APPS.append('features')
INSTALLED_APPS.append('test_utils')

ACCEPTANCE_TESTING = True

JWT_EXPIRATION_DELTA_IN_DAYS = environ.get('JWT_EXPIRATION_DELTA_IN_DAYS')
JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS = environ.get(
    'JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS')
JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
JWT_ALGORITHM = environ.get('JWT_ALGORITHM')

if JWT_EXPIRATION_DELTA_IN_DAYS is None or JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS is None or JWT_SECRET_KEY is None or JWT_ALGORITHM is None:
    raise Exception('Graphql JWT parameters not defined.')

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=int(JWT_EXPIRATION_DELTA_IN_DAYS)),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=int(JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS)),
    'JWT_SECRET_KEY': JWT_SECRET_KEY,
    'JWT_ALGORITHM': JWT_ALGORITHM
}

DOMAIN_NAME = "shopozor.ch"
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

PASSWORD_RESET_TIMEOUT_DAYS = 1

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "ERROR", "handlers": ["console"]},
    "formatters": {
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    }
}

FIXTURE_DIRS = [os.path.join('features', 'fixtures')]
