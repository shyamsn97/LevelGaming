# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-11 23:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poppin', '0003_auto_20170911_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='content',
            field=models.CharField(default='', max_length=900000),
        ),
    ]