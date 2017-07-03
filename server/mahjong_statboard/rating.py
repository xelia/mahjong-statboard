# -*- coding: utf-8 -*-
from collections import Counter


class AbstractRating(object):
    def __init__(self, instance):
        self.instance = instance

    def get_games(self):
        return self.instance.get_games()

    def get_rating(self, player):
        raise NotImplementedError


class AveragePlace(AbstractRating):
    def get_rating(self, player):
        result = Counter()
        games = Counter()

        for game in self.get_games():
            for game_player, game_result in game['final_results'].items():
                result[game_player] += game_result['place']
                games[game_player] += 1
        print(result)
        print(games)
        print(player, result[player], games[player])
        return result[player] / games[player] if player in result else None

