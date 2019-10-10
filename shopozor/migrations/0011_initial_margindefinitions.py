from django.conf import settings
from django.db import migrations, models


def add_initial_margin_defns(apps, schema_editor):
    if hasattr(settings, 'ACCEPTANCE_TESTING'):
        # in the case of acceptance testing, the permissions are
        # set as fixtures; after every scenario, those permissions
        # are cleared up
        # would we set them here up, they would just be gone after the
        # first test
        return

    margindefns_model = apps.get_model('shopozor', 'MarginDefinitions')
    margindefns_model.objects.create(
        role='manager', margin=settings.MANAGER_MARGIN * 100)
    margindefns_model.objects.create(
        role='rex', margin=settings.REX_MARGIN * 100)
    margindefns_model.objects.create(
        role='softozor', margin=settings.SOFTOZOR_MARGIN * 100)


class Migration(migrations.Migration):

    dependencies = [
        ('shopozor', '0010_margindefinitions'),
    ]

    operations = [
        migrations.RunPython(add_initial_margin_defns)
    ]
