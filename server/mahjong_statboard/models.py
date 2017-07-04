# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import get_user_model

from mahjong_statboard import backends


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

    @property
    def backend(self):
        if self.game_storage == self.STORAGE_PANTHEON:
            return backends.PantheonBackend()
        else:
            return backends.LocalBackend()


class Rating(models.Model):
    instance = models.ForeignKey(Instance)
    rating_type = models.CharField(max_length=32)


class Stats(models.Model):
    instance = models.ForeignKey(Instance)
    rating = models.ForeignKey(Rating)
    player = models.TextField()
    value = models.TextField()
    game = models.TextField()


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
