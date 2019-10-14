from django.db import migrations, models
from django.conf import settings
from django_prices_vatlayer import utils


def add_initial_vat_rates(apps, schema_editor):
    if hasattr(settings, 'ACCEPTANCE_TESTING'):
        # in the case of acceptance testing, the permissions are
        # set as fixtures; after every scenario, those permissions
        # are cleared up
        # would we set them here up, they would just be gone after the
        # first test
        return

    rates = {
        'success': True,
        'rates': {
            'CH': {
                'country_name': 'Switzerland',
                'standard_rate': settings.VAT_SERVICES * 100,
                'reduced_rates': {
                    'reduced': settings.VAT_PRODUCTS * 100,
                    'special': settings.VAT_SPECIAL * 100
                }
            }
        }
    }
    utils.create_objects_from_json(rates)


def add_initial_vat_rate_types(apps, schema_editor):
    if hasattr(settings, 'ACCEPTANCE_TESTING'):
        # in the case of acceptance testing, the permissions are
        # set as fixtures; after every scenario, those permissions
        # are cleared up
        # would we set them here up, they would just be gone after the
        # first test
        return

    rate_types = {'success': True, 'types': ['reduced', 'special']}
    utils.save_vat_rate_types(rate_types)


class Migration(migrations.Migration):

    dependencies = [
        ('shopozor', '0012_auto_20191010_0336'),
    ]

    operations = [
        migrations.RunPython(add_initial_vat_rates),
        migrations.RunPython(add_initial_vat_rate_types)
    ]
