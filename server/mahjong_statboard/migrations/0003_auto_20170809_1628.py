# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mahjong_statboard', '0002_auto_20170731_1136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'ordering': ('weight',)},
        ),
        migrations.AddField(
            model_name='rating',
            name='rating_name',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]
