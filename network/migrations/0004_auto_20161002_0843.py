# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 08:43
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20160710_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_name',
            field=models.CharField(max_length=25, validators=[django.core.validators.RegexValidator(message='Invalid name', regex='^[-a-zA-Z0-9]{1,25}$')]),
        ),
    ]
