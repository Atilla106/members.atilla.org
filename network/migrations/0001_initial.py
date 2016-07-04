# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-04 00:37
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(max_length=25, validators=[django.core.validators.RegexValidator(message='Invalid name', regex='^[a-zA-Z0-9_−]{1,25}$')])),
                ('device_ip', models.GenericIPAddressField(protocol='IPv4', unique=True)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='Date added')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last update')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interface_type', models.CharField(choices=[('WLP', 'Wifi'), ('ETH', 'Ethernet')], default='ETH', max_length=3)),
                ('mac_address', models.CharField(max_length=17, unique=True, validators=[django.core.validators.RegexValidator(message='Invalid MAC address', regex='^([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})$')])),
                ('description', models.CharField(blank=True, max_length=255)),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='Date added')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last update')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.Device')),
            ],
        ),
    ]
