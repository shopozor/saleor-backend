# Generated by Django 2.2.3 on 2019-09-11 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopozor', '0008_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
