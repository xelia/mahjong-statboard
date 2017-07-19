# -*- coding: utf-8 -*-
import json
from collections import Counter, defaultdict

from mahjong_statboard import models


class AbstractRating(object):
    name = 'Abstract rating'

    def __init__(self, rating):
        self.rating = rating

    def get_games(self):
        return self.rating.instance.game_set.prefetch_related('gameresult_set').all()

    def save_rating(self, player, value):
        stat, _ = models.Stats.objects.get_or_create(instance=self.rating.instance, rating=self.rating, player=player)
        stat.value = value
        stat.save()

    def process(self):
        raise NotImplementedError()


class AveragePlace(AbstractRating):
    name = 'Average place'

    def process(self):
        result = Counter()
        games = Counter()

        for game in self.get_games():
            for game_result in game.gameresult_set.all():
                result[game_result.player] += game_result.place
                games[game_result.player] += 1

        for player in result:
            self.save_rating(player, round(result[player] / games[player], 3))


class AveragePlaceSeries(AbstractRating):
    name = '10 games series'
    series_len = 10

    def format_series(self, series):
        return {
            'avg_place': sum(result.place for result in series) / len(series),
            'score_sum': sum(result.score for result in series),
            'series': [result.place for result in series]
        }

    def process(self):
        series_dict = defaultdict(list)
        best_series_dict = {}

        for game in self.get_games():
            for game_result in game.gameresult_set.all():
                series = series_dict[game_result.player]
                series.append(game_result)
                if len(series) > self.series_len:
                    series.pop(0)
                if len(series) < self.series_len:
                    continue
                series = self.format_series(series)
                best_series = best_series_dict.get(game_result.player)
                if not best_series or series['avg_place'] < best_series['avg_place'] or\
                        series['avg_place'] == best_series['avg_place'] and series['score_sum'] > best_series['score_sum']:
                    best_series_dict[game_result.player] = series

        for player in best_series_dict:
            self.save_rating(
                player,
                json.dumps({
                    'best': best_series_dict[player],
                    'current': self.format_series(series_dict[player])
                })
            )

ALL_RATINGS = {r.name: r for r in (AveragePlace, AveragePlaceSeries)}
