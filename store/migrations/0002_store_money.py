# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 08:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='money',
            field=models.PositiveIntegerField(default=1000),
        ),
    ]
