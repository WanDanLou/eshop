# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-08 04:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20170708_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='不知道怎么分类', max_length=200),
        ),
    ]