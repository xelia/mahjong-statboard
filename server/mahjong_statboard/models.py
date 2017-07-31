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
    rating_type_id = models.CharField(max_length=32, choices=((r.id, r.name) for r in rating.ALL_RATINGS.values()))
    series_len = models.PositiveIntegerField(blank=True, null=True, help_text='Работает только если рейтинг является серией')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    weight = models.IntegerField(help_text='Порядок сортировки')

    def __str__(self):
        res = '{}: {}'.format(self.instance.name, self.rating_type_id)
        if self.start_date:
            res += ' start: {}'.format(self.start_date)
        if self.end_date:
            res += ' end: {}'.format(self.end_date)
        if self.series_len:
            res += ' length: {}'.format(self.series_len)
        return res


class Stats(models.Model):
    instance = models.ForeignKey(Instance)
    rating = models.ForeignKey(Rating)
    player = models.ForeignKey('Player')
    value = models.TextField()
    place = models.IntegerField(null=True, blank=True)
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
            result = result[0] if result else None
        return result

    def __str__(self):
        return '{}, {}, {}, {}: {}'.format(self.instance.name, self.rating, self.player, self.game, self.value)


class Player(models.Model):
    instance = models.ForeignKey(Instance)
    name = models.CharField(max_length=256)
    full_name = models.TextField(blank=True)

    class Meta:
        unique_together = ('instance', 'name')

    def __str__(self):
        return 'Player: {}'.format(self.name)


class Game(models.Model):
    instance = models.ForeignKey(Instance)
    date = models.DateField()
    addition_time = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(get_user_model(), null=True)

    def __str__(self):
        return 'Game date: {}'.format(self.date)


class GameResult(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)
    score = models.IntegerField()
    place = models.SmallIntegerField()
    starting_position = models.SmallIntegerField()
