from datetime import timedelta
from saleor.settings import *

import os

if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware',
                       'django.middleware.common.CommonMiddleware']
    MIDDLEWARE = CORS_MIDDLEWARE + MIDDLEWARE
    INSTALLED_APPS.append('corsheaders')

INSTALLED_APPS.remove('saleor.graphql')
INSTALLED_APPS.append('shopozor')

ROOT_URLCONF = 'shopozor.urls'

GRAPHQL_JWT = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=30),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=360),
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALGORITHM': 'HS256'
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'shopozor.password_validation.SpecialCharacterValidator',
    },
    {
        'NAME': 'shopozor.password_validation.NumberAndLetterValidator',
    }
]

TEST_RUNNER = "unit_tests.runner.PytestTestRunner"

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "CH")
DEFAULT_CURRENCY = os.getenv("DEFAULT_CURRENCY", "CHF")

WSGI_APPLICATION = "shopozor.wsgi.application"

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')

if EMAIL_BACKEND == 'django.core.mail.backends.filebased.EmailBackend':
    EMAIL_FILE_PATH = os.getenv('EMAIL_FILE_PATH')
