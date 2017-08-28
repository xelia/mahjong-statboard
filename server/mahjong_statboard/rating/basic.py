import json
from collections import Counter

from django.db import transaction

from mahjong_statboard import models
from mahjong_statboard.rating.backends import AbstractBackend


class AbstractRating(object):
    id = 'abstract_rating'
    name = 'Abstract rating'
    is_series = False

    def __init__(self, rating: 'models.Rating', backend: AbstractBackend):
        self.rating = rating
        self.backend = backend

    def _sortkey(self, value):
        return value

    def save_rating(self, player, value, place):
        stat, _ = models.Stats.objects.get_or_create(instance=self.rating.instance, rating=self.rating, player=player, place=place)
        stat.value = json.dumps(value)
        stat.save()

    def process(self):
        raise NotImplementedError()

    def process_and_save(self):
        sorted_rating = sorted(self.process().items(), key=lambda a: self._sortkey(a[1]))
        with transaction.atomic():
            models.Stats.objects.filter(instance=self.rating.instance, rating=self.rating).delete()
            for place, (player, value) in enumerate(sorted_rating, start=1):
                self.save_rating(player, value, place)

    def get_game_results(self):
        return self.backend.get_game_results(self.rating.start_date, self.rating.end_date)


class AveragePlace(AbstractRating):
    id = 'average_place'
    name = 'Среднее место'

    def process(self):
        result = Counter()
        games = Counter()

        for game_result in self.backend.get_game_results():
            result[game_result.player] += game_result.place
            games[game_result.player] += 1

        return {player: round(result[player] / games[player], 3) for player in result}


class GamesCount(AbstractRating):
    id = 'games_count'
    name = 'Число игр'

    def process(self):
        result = Counter()

        for game_result in self.backend.get_game_results():
            result[game_result.player] += 1

        return result


class AverageScore(AbstractRating):
    id = 'average_score'
    name = 'Средний счет'

    def process(self):
        result = Counter()
        games = Counter()

        for game_result in self.backend.get_game_results():
            result[game_result.player] += game_result.score
            games[game_result.player] += 1

        return {player: round(result[player] / games[player]) for player in result}


class MaxScore(AbstractRating):
    id = 'max_score'
    name = 'Максимальный счет'

    def process(self):
        result = Counter()

        for game_result in self.backend.get_game_results():
            result[game_result.player] = max(game_result.score, result[game_result.player])

        return result


class ScoreSum(AbstractRating):
    id = 'max_score'
    name = 'Сумма очков'

    def process(self):
        result = Counter()

        for game_result in self.backend.get_game_results():
            result[game_result.player] += game_result.score - 25000

        return result
