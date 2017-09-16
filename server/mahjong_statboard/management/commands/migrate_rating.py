import csv
import datetime

import requests
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from mahjong_statboard import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        instance, _ = models.Instance.objects.get_or_create(name='tesuji_rating')
        with transaction.atomic():
            if instance.game_set.count():
                print('Games exist, deleting')
                models.GameResult.objects.filter(game__instance=instance).delete()
                models.Game.objects.filter(instance=instance).delete()
                # print('Games exist, exiting')
                # return
            print('Fetching games')
            lines = list(csv.reader(
                requests.get('http://old-rating.tesuji.ru/games_csv2', stream=True).iter_lines(decode_unicode=True),
                delimiter=';'
            ))
            for line in lines[::-1]:
                date, player1, score1, player2, score2, player3, score3, player4, score4, addition_date, posted_by = line
                players = [player1, player2, player3, player4]
                scores = [int(score1), int(score2), int(score3), int(score4)]
                places = [sum(score <= other_score for other_score in scores) for score in scores]
                if set(places) != {1, 2, 3, 4}:
                    for place in (1, 2, 3, 4):
                        if place not in places:
                            places[places.index(place + 1)] -= 1
                posted_by, _ = get_user_model().objects.get_or_create(username=posted_by)
                game = models.Game.objects.create(
                    instance=instance,
                    date=datetime.datetime.strptime(date, '%d.%m.%Y'),
                    posted_by=posted_by,
                )
                game.addition_time = datetime.datetime.strptime(addition_date, '%Y-%m-%dT%H:%M:%S.%f+00:00')
                game.save()
                for player_name, score, place, starting_position in zip(players, scores, places, (1,2,3,4)):
                    player, _ = models.Player.objects.get_or_create(instance=instance, name=player_name)
                    gr, _ = models.GameResult.objects.get_or_create(
                        game=game,
                        player=player,
                        place=place,
                        score=score,
                        starting_position=starting_position
                    )
                print(players, scores)

            print('Fetching players')
            r = requests.get('http://rating.tesuji.ru/players_csv', stream=True)
            r.encoding = 'UTF-8'
            lines = list(csv.reader(
                r.iter_lines(decode_unicode=True),
                delimiter=';'
            ))
            for line in lines:
                print(line)
                name, full_name, hidden = line
                try:
                    player = models.Player.objects.get(instance=instance, name=name)
                    player.full_name = full_name.strip()
                    player.hidden = hidden
                    player.save()
                except models.Player.DoesNotExist:
                    pass
