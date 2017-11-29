import datetime
import json
from collections import Counter, defaultdict

from django.db import transaction

from mahjong_statboard import models
from mahjong_statboard.rating.backends import AbstractBackend


class AbstractRating(object):
    id = 'abstract_rating'
    name = 'Abstract rating'
    is_series = False
    reverse_sort = False

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
        sorted_rating = sorted(self.process().items(), key=lambda a: self._sortkey(a[1]), reverse=self.reverse_sort)
        with transaction.atomic():
            models.Stats.objects.filter(instance=self.rating.instance, rating=self.rating).delete()
            for place, (player, value) in enumerate(sorted_rating, start=1):
                self.save_rating(player, value, place)

    def get_game_results(self):
        return self.backend.get_game_results(self.rating.start_date, self.rating.end_date, self.rating.days_number)


class AveragePlace(AbstractRating):
    id = 'average_place'
    name = 'Среднее место'

    def process(self):
        result = Counter()
        games = Counter()

        for game_result in self.get_game_results():
            result[game_result.player] += game_result.place
            games[game_result.player] += 1

        return {player: round(result[player] / games[player], 3) for player in result if games[player] >= 10}


class GamesCount(AbstractRating):
    id = 'games_count'
    name = 'Число игр'
    reverse_sort = True

    def process(self):
        result = Counter()

        for game_result in self.get_game_results():
            result[game_result.player] += 1

        return result


class AverageScore(AbstractRating):
    id = 'average_score'
    name = 'Средний счет'
    reverse_sort = True

    def process(self):
        result = Counter()
        games = Counter()

        for game_result in self.get_game_results():
            result[game_result.player] += game_result.score
            games[game_result.player] += 1

        return {player: round(result[player] / games[player]) for player in result if games[player] >= 10}


class MaxScore(AbstractRating):
    id = 'max_score'
    name = 'Максимальный счет'
    reverse_sort = True

    def process(self):
        result = Counter()

        for game_result in self.get_game_results():
            result[game_result.player] = max(game_result.score, result[game_result.player])

        return result


class ScoreSum(AbstractRating):
    id = 'score_sum'
    name = 'Сумма очков'
    reverse_sort = True

    def process(self):
        result = Counter()

        for game_result in self.get_game_results():
            result[game_result.player] += game_result.score - 25000

        return result


class LastGameDate(AbstractRating):
    id = 'last_game_date'
    name = 'Дата последней игры'
    reverse_sort = True

    def process(self):
        result = defaultdict(lambda: datetime.date.min)

        for game_result in self.get_game_results():
            result[game_result.player] = max(game_result.game.date, result[game_result.player])

        result = {key: value.strftime('%Y.%m.%d') for key, value in result.items()}
        return result
