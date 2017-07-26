# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 11:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('addition_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('place', models.SmallIntegerField()),
                ('starting_position', models.SmallIntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mahjong_statboard.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Instance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('game_storage', models.CharField(choices=[('local', 'local'), ('pantheon', 'pantheon')], default='local', max_length=16)),
                ('pantheon_id', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('full_name', models.TextField(blank=True)),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mahjong_statboard.Instance')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_type', models.CharField(choices=[('Average place', 'Average place'), ('Average place/Score sum series', 'Average place/Score sum series')], max_length=32)),
                ('series_len', models.PositiveIntegerField(blank=True, help_text='Работает только если рейтинг является серией', null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('weight', models.IntegerField(help_text='Порядок сортировки')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mahjong_statboard.Instance')),
            ],
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('game', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mahjong_statboard.Game')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mahjong_statboard.Instance')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mahjong_statboard.Player')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mahjong_statboard.Rating')),
            ],
        ),
        migrations.AddField(
            model_name='gameresult',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mahjong_statboard.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mahjong_statboard.Instance'),
        ),
        migrations.AddField(
            model_name='game',
            name='posted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
