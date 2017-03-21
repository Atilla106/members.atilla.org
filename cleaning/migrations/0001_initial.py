# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0005_account_cleaning'),
    ]

    operations = [
        migrations.CreateModel(
            name='CleaningRoster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('cleaners', models.ManyToManyField(to='accounts.Account')),
            ],
        ),
    ]
