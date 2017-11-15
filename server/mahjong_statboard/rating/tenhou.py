# -*- coding: utf-8 -*-
from collections import defaultdict, Counter
from itertools import groupby

from mahjong_statboard.rating.basic import AbstractRating


class TenhouRating(AbstractRating):
    id = 'tenhou_rating'
    name = 'Tenhou rating'
    base = [30, 10, -10, -30]
    use_adjustement = True

    def _sortkey(self, value):
        return -value

    def process(self):
        rating = defaultdict(lambda: 1500)
        games_played = Counter()
        for game_id, game_results in groupby(self.get_game_results(), lambda a: a.game_id):
            game_results = list(game_results)
            atr = sum(rating[gr.player] for gr in game_results) / 4
            for game_result in game_results:
                if self.use_adjustement:
                    adj = max(0.2, 1 - games_played[game_result.player] * 0.002)
                else:
                    adj = 1
                change = adj * (self.base[game_result.place - 1] + (atr - rating[game_result.player]) / 40)
                rating[game_result.player] += change
                games_played[game_result.player] += 1
        rating = {p: round(r, 2) for p, r in rating.items()}
        return rating


class TenhouRatingNoAdj(TenhouRating):
    id = 'tenhou_rating_no_adj'
    name = 'Tenhou rating(без затухания)'
    use_adjustement = False

