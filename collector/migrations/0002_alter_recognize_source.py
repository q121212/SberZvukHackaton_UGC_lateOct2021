# Generated by Django 3.2.8 on 2021-10-30 11:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collector', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recognize',
            name='source',
            field=models.URLField(validators=[django.core.validators.URLValidator(schemes=['http'])]),
        ),
    ]
