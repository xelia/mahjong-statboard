# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import get_user_model

from mahjong_statboard.pantheon import PantheonClient


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

    def get_games(self):
        if self.game_storage == self.STORAGE_PANTHEON:
            return PantheonClient().get_last_games(self.pantheon_id)['games']


class Game(models.Model):
    instance = models.ForeignKey(Instance)
    date = models.DateField()
    player1 = models.TextField()
    player2 = models.TextField()
    player3 = models.TextField()
    player4 = models.TextField()
    score1 = models.FloatField()
    score2 = models.FloatField()
    score3 = models.FloatField()
    score4 = models.FloatField()
    addition_time = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(get_user_model(), null=True)

    def __str__(self):
        return 'Game date: {}'.format(self.date)


class Rating(models.Model):
    instance = models.ForeignKey(Instance)
    rating_type = models.CharField(max_length=32)


class Stats(models.Model):
    instance = models.ForeignKey(Instance)
    rating = models.ForeignKey(Rating)
    player = models.TextField()
    value = models.TextField()
    game = models.ForeignKey(Game)
