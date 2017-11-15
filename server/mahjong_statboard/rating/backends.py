from datetime import date, timedelta

from mahjong_statboard import models


class AbstractBackend(object):
    def __init__(self, instance):
        self.instance = instance

    def get_game_results(self, start_date=None, end_date=None, days_number=None):
        raise NotImplementedError()


class LocalBackend(AbstractBackend):
    def get_game_results(self, start_date=None, end_date=None, days_number=None):
        result = models.GameResult.objects.filter(
            game__instance__id=self.instance.id
        ).order_by(
            'game__date',
            'game__addition_time'
        ).select_related(
            'player'
        )
        if start_date:
            result = result.filter(game__date__gte=start_date)
        if end_date:
            result = result.filter(game__date__lte=end_date)
        if days_number:
            result = result.filter(game__date__gte=date.today() - timedelta(days=days_number))
        return result.all()