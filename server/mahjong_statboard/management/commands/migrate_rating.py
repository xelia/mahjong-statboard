import csv
import datetime

import requests
from django.core.management.base import BaseCommand
from django.db import transaction

from mahjong_statboard import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        instance, _ = models.Instance.objects.get_or_create(name='tesuji_rating')
        lines = list(csv.reader(
            requests.get('http://rating.tesuji.ru/games_csv', stream=True).iter_lines(decode_unicode=True),
            delimiter=';'
        ))
        with transaction.atomic():
            for line in lines[::-1]:
                date, player1, score1, player2, score2, player3, score3, player4, score4 = line
                players = [player1, player2, player3, player4]
                scores = [int(score1), int(score2), int(score3), int(score4)]
                places = [sum(score <= other_score for other_score in scores) for score in scores]
                if set(places) != {1, 2, 3, 4}:
                    for place in (1, 2, 3, 4):
                        if place not in places:
                            places[places.index(place + 1)] -= 1

                game = models.Game.objects.create(
                    instance=instance,
                    date=datetime.datetime.strptime(date, '%d.%m.%Y'),
                )
                for player, score, place, starting_position in zip(players, scores, places, (1,2,3,4)):
                    gr, _ = models.GameResult.objects.get_or_create(
                        game=game,
                        player=player,
                        place=place,
                        score=score,
                        starting_position=starting_position
                    )
                print(players, scores)
