import json
from collections import defaultdict

from mahjong_statboard.rating.basic import AbstractRating


class AbstractSeries(AbstractRating):
    name = 'Abstract series'

    @property
    def series_len(self):
        return self.rating.series_len or 0

    def format_series(self, series):
        raise NotImplementedError()

    def get_best_series(self, *series_list):
        raise NotImplementedError()

    def process(self):
        series_dict = defaultdict(list)
        best_series_dict = {}

        for game_result in self.backend.get_game_results():
            series = series_dict[game_result.player]
            series.append(game_result)
            if len(series) > self.series_len:
                series.pop(0)
            if len(series) < self.series_len:
                continue
            series = self.format_series(series)
            best_series_dict[game_result.player] = self.get_best_series(best_series_dict.get(game_result.player), series)

        return {
            player: {
                'best': best_series_dict[player],
                'current': self.format_series(series_dict[player])
            } for player in best_series_dict
        }


class AveragePlaceSeries(AbstractSeries):
    name = 'Average place/Score sum series'

    def get_best_series(self, *series_list):
        series_list = filter(None, series_list)
        return max(series_list, key=lambda a: (-a['avg_place'], a['score_sum']))

    def format_series(self, series):
        return {
            'avg_place': sum(result.place for result in series) / len(series),
            'score_sum': sum(result.score for result in series),
            'series': [result.place for result in series]
        }