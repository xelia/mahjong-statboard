# -*- coding: utf-8 -*-
import json
from collections import defaultdict
from django.db import models
from django.contrib.auth import get_user_model

from mahjong_statboard import rating


class Instance(models.Model):
    STORAGE_LOCAL = 'local'
    STORAGE_PANTHEON = 'pantheon'
    STORAGE_CHOICES = (
        (STORAGE_LOCAL, STORAGE_LOCAL),
        (STORAGE_PANTHEON, STORAGE_PANTHEON),
    )
    name = models.TextField()
    description = models.TextField(blank=True)
    game_storage = models.CharField(max_length=16, choices=STORAGE_CHOICES, default=STORAGE_LOCAL)
    pantheon_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    instance = models.ForeignKey(Instance)
    rating_type = models.CharField(max_length=32, choices=((r, r) for r in rating.ALL_RATINGS))
    series_len = models.PositiveIntegerField(blank=True, null=True, help_text='Работает только если рейтинг является серией')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    weight = models.IntegerField(help_text='Порядок сортировки')

    def __str__(self):
        return '{}: {}'.format(self.instance.name, self.rating_type)


class Stats(models.Model):
    instance = models.ForeignKey(Instance)
    rating = models.ForeignKey(Rating)
    player = models.TextField()
    value = models.TextField()
    game = models.ForeignKey('Game', null=True)

    @classmethod
    def get_player_stats(cls, instance_id, player=None):
        stats = cls.objects.filter(instance_id=instance_id)
        if player:
            stats = stats.filter(player=player)
        result = defaultdict(dict)
        for stat in stats.all():
            result[stat.player][stat.rating_id] = json.loads(stat.value)
        result = [{'player': pl, 'stats': st} for pl, st in result.items()]
        if player:
            result = result[0]
        return result

    def __str__(self):
        return '{}, {}, {}, {}: {}'.format(self.instance.name, self.rating, self.player, self.game, self.value)


# Tables for local backend
class Game(models.Model):
    instance = models.ForeignKey(Instance)
    date = models.DateField()
    addition_time = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(get_user_model(), null=True)

    def __str__(self):
        return 'Game date: {}'.format(self.date)


class GameResult(models.Model):
    game = models.ForeignKey(Game)
    player = models.TextField()
    score = models.IntegerField()
    place = models.SmallIntegerField()
    starting_position = models.SmallIntegerField()
