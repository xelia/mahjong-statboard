import json
from collections import Counter

from mahjong_statboard import models
from mahjong_statboard.rating.backends import AbstractBackend


class AbstractRating(object):
    name = 'Abstract rating'

    def __init__(self, rating: 'models.Rating', backend: AbstractBackend):
        self.rating = rating
        self.backend = backend

    def save_rating(self, player, value):
        stat, _ = models.Stats.objects.get_or_create(instance=self.rating.instance, rating=self.rating, player=player)
        stat.value = json.dumps(value)
        stat.save()

    def process(self):
        raise NotImplementedError()

    def process_and_save(self):
        for player, value in self.process().items():
            self.save_rating(player, value)

    def get_game_results(self):
        return self.backend.get_game_results(self.rating.start_date, self.rating.end_date)


class AveragePlace(AbstractRating):
    name = 'Average place'

    def process(self):
        result = Counter()
        games = Counter()

        for game_result in self.get_game_results():
            result[game_result.player] += game_result.place
            games[game_result.player] += 1

        return {player: round(result[player] / games[player], 3) for player in result}


class GamesCount(AbstractRating):
    name = 'Games count'

    def process(self):
        result = Counter()