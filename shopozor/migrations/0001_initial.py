from django.db import migrations
from django.conf import settings

from shopozor.permissions import add_permissions


def add_shopozor_permissions(apps, schema_editor):
    if hasattr(settings, 'ACCEPTANCE_TESTING'):
        # in the case of acceptance testing, the permissions are
        # set as fixtures; after every scenario, those permissions
        # are cleared up
        # would we set them here up, they would just be gone after the
        # first test
        return

    user_model = apps.get_model('account', 'User')
    permission_model = apps.get_model('auth', 'Permission')
    content_type_model = apps.get_model('contenttypes', 'ContentType')
    add_permissions(user_model, permission_model, content_type_model)


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0024_auto_20181011_0737'),
        ('auth', '0009_alter_user_last_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name')
    ]

    operations = [
        migrations.RunPython(add_shopozor_permissions)
    ]
