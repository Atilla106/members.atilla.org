# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 01:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20160710_0113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='device',
            options={'permissions': (('can_publish_device', 'Can use this device on the network'),)},
        ),
    ]
