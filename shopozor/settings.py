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
    },
    # This must be last in list because an exception is raised if the site is inacessible
    {
        'NAME': 'shopozor.password_validation.HasBeenPwndValidator',
    },
]

TEST_RUNNER = "unit_tests.runner.PytestTestRunner"

# We need to configure the EMAIL_URL and everything following
# For now on and for local purpose, we set the following variable
DOMAIN_NAME = "shopozor.ch"
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
"""
EMAIL_URL = os.environ.get("EMAIL_URL")
SENDGRID_USERNAME = os.environ.get("SENDGRID_USERNAME")
SENDGRID_PASSWORD = os.environ.get("SENDGRID_PASSWORD")
if not EMAIL_URL and SENDGRID_USERNAME and SENDGRID_PASSWORD:
    EMAIL_URL = "smtp://%s:%s@smtp.sendgrid.net:587/?tls=True" % (
        SENDGRID_USERNAME,
        SENDGRID_PASSWORD,
    )
email_config = dj_email_url.parse(EMAIL_URL or "console://")

EMAIL_FILE_PATH = email_config["EMAIL_FILE_PATH"]
EMAIL_HOST_USER = email_config["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = email_config["EMAIL_HOST_PASSWORD"]
EMAIL_HOST = email_config["EMAIL_HOST"]
EMAIL_PORT = email_config["EMAIL_PORT"]
EMAIL_BACKEND = email_config["EMAIL_BACKEND"]
EMAIL_USE_TLS = email_config["EMAIL_USE_TLS"]
EMAIL_USE_SSL = email_config["EMAIL_USE_SSL"]

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
"""
