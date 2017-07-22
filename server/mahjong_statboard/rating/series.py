import json
from collections import defaultdict

from mahjong_statboard.rating.basic import AbstractRating


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

        for game_result in self.backend.get_game_results():
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

        return {
            player: json.dumps({
                'best': best_series_dict[player],
                'current': self.format_series(series_dict[player])
            }) for player in best_series_dict
        }