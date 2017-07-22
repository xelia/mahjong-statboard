from mahjong_statboard import models


class AbstractBackend(object):
    def __init__(self, instance):
        self.instance = instance

    def get_game_results(self):
        raise NotImplementedError()


class LocalBackend(AbstractBackend):
    def get_game_results(self):
        result = models.GameResult.objects.filter(
            game__instance__id=self.instance.id
        ).order_by(
            'game__date',
            'game__addition_time'
        )
        return result.all()