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
                game, _ = models.Game.objects.get_or_create(
                    instance=instance,
                    date=datetime.datetime.strptime(date, '%d.%m.%Y'),
                    player1=player1,
                    player2=player2,
                    player3=player3,
                    player4=player4,
                    score1=score1,
                    score2=score2,
                    score3=score3,
                    score4=score4,
                )
                print(game, _)
