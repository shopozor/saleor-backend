from django.core.wsgi import get_wsgi_application
import os
import sys

activationScriptFilename = os.path.join(
    'PATH_TO_VIRTUAL_ENV_PLACEHOLDER', 'bin', 'activate_this.py')
try:
    # the PATH_TO_VIRTUAL_ENV variable is defined by our jps
    exec(open(activationScriptFilename).read())
except IOError:
    sys.stderr.write("Couldn't read file: ", activationScriptFilename)

sys.path.append(os.path.join(os.environ['HOME'], 'ROOT'))
sys.path.append(os.path.join(os.environ['HOME'], 'ROOT', 'saleor'))
os.environ['SECRET_KEY'] = 'SECRET_KEY_PLACEHOLDER'
os.environ['ALLOWED_HOSTS'] = 'ALLOWED_HOSTS_PLACEHOLDER'
os.environ['DATABASE_URL'] = 'DATABASE_URL_PLACEHOLDER'
os.environ['CACHE_URL'] = 'CACHE_URL_PLACEHOLDER'

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'DJANGO_SETTINGS_MODULE_PLACEHOLDER')

application = get_wsgi_application()
