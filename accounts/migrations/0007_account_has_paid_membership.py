# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-09-20 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20170325_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='has_paid_membership',
            field=models.BooleanField(default=False),
        ),
    ]
