# Generated by Django 2.2.3 on 2019-08-17 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopozor', '0005_shop_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='latitude',
            field=models.DecimalField(
                decimal_places=6, default=46.775501, max_digits=9),
        ),
        migrations.AddField(
            model_name='shop',
            name='longitude',
            field=models.DecimalField(
                decimal_places=6, default=7.037878, max_digits=9),
        ),
    ]
