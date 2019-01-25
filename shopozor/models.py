from django.db import models
from saleor.core.permissions import MODELS_PERMISSIONS
# from saleor.account.models import User
# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType

MODELS_PERMISSIONS.append('shopozor.manage_producers')
MODELS_PERMISSIONS.append('shopozor.manage_managers')
MODELS_PERMISSIONS.append('shopozor.manage_rex')

# ct = ContentType.objects.get_for_model(User)
# Permission.objects.create(codename='manage_producers', name='Can manage producers', content_type=ct)
# Permission.objects.create(codename='manage_managers', name='Can manage managers', content_type=ct)
# Permission.objects.create(codename='manage_rex', name='Can manage rex', content_type=ct)

# Create your models here.
print('wooooooo')
