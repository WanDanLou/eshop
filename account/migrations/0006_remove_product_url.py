# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 12:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20170702_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='url',
        ),
    ]
