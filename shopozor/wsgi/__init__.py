"""WSGI config for Shopozor project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.
"""
import os

from django.core.wsgi import get_wsgi_application

from saleor.wsgi.health_check import health_check

os.environ['DJANGO_SETTINGS_MODULE'] = 'shopozor.settings'
# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()
application = health_check(application, "/health/")

print("TROUDUC")
# TODO: before calling  uwsgi --ini shopozor/wsgi/uwsgi.ini
# TODO: do export DJANGO_SETTINGS_MODULE=shopozor.settings
# TODO: do export PORT=8000
# TODO: apparently, shopozor.settings is not called at all
