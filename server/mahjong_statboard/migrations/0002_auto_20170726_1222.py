# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 12:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mahjong_statboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([('instance', 'name')]),
        ),
    ]
