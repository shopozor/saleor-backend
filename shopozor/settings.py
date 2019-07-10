from saleor.settings import *
from datetime import timedelta
import dj_email_url

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

# We need to configure the EMAIL_URL and everything following
# For now on and for local purpose, we set the following variable
DOMAIN_NAME = "shopozor.ch"
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'