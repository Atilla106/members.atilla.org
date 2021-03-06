# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-30 22:15
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20161002_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_name',
            field=models.CharField(max_length=25, validators=[django.core.validators.RegexValidator(message="Le nom d'appareil ne peut pas contenir autre chose que des caractères alphanumériques et '-' ", regex='^[-a-zA-Z0-9]{1,25}$')]),
        ),
        migrations.AlterField(
            model_name='interface',
            name='mac_address',
            field=models.CharField(max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message="L'addresse mac doit être du format xx:xx:xx:xx:xx:xx,et ne doit comprendre que des caractères dans 1-9 eta-f", regex='^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$')]),
        ),
    ]
