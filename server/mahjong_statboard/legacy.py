# -*- coding: utf-8 -*-
import datetime
import logging
from django.db import transaction

from mahjong_statboard import models


def add_games(raw_games, instance, user):
    try:
        return do_add_games(raw_games, instance, user)
    except Exception as e:
        return str(e)


@transaction.atomic
def do_add_games(raw_games, instance, user):
    res = ""
    linenum = errors = 0
    for line in raw_games.split("\n"):
        linenum += 1
        res += "Line #" + str(linenum) + ": "
        if line.startswith('http'):
            continue
            # try:
            #     date, players, scores = import_from_replay(line)
            # except Exception, e:
            #     logging.exception('')
            #     res += "Error importing replay: {}".format(e)
            #     errors += 1
            #     continue
        else:
            words = line.split(" ")
            if len(words) == 10 and words[9][-1] == chr(13):
                words[9] = words[9][:-1]
            if len(words) != 9:
                res += "Error: Data format error <br>"
                errors += 1
                continue

            dt = list(map(int, words[0].split(".")))
            if dt[2] < 1000:
                dt[2] += 2000
            date = datetime.date(dt[2], dt[1], dt[0])
            players = list(words[1::2])
            scores = map(int, words[2::2])
        game = models.Game.objects.create(date=date, posted_by=user, instance=instance)
        places = [len([s for s in scores if s > score]) for score in scores]

        if sum(scores) == 0:
            scores = [i + 25000 for i in scores]
        if sum(scores) != 100000:
            res += "Error: Total score error. The sum is %s <br>" % sum(scores)
            errors += 1
            continue

        for num, player, score, place in zip(range(4), players, scores, places):
            player, created = models.Player.objects.get_or_create(instance=instance, name=player)
            game_result = models.GameResult.objects.create(player=player, game=game, starting_position=num + 1, score=score, place=0)
            game_result.save()
        for place, game_result in enumerate(game.gameresult_set.order_by('-score', 'starting_position').all()):
            game_result.place = place + 1
            game_result.save()
        game.save()
        res += "OK <br>"
    if errors == 0:
        res = "Данные добавлены. <br>" + res
        logger = logging.getLogger('add_games')
        logger.info('Games added')
        logger.info(raw_games)
    else:
        res = "Во входных данных обнаружены ошибки. Данные не добавлены. <br>" + res
        raise Exception(res)
    return res