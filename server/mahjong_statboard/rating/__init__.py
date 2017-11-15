import logging

from django.db import transaction

from mahjong_statboard import models
from mahjong_statboard.rating.basic import AveragePlace, AbstractRating, AverageScore, GamesCount, MaxScore, ScoreSum
from mahjong_statboard.rating.series import AveragePlaceSeries
from mahjong_statboard.rating.tenhou import TenhouRating, TenhouRatingNoAdj

ALL_RATINGS = {r.id: r for r in (AveragePlace, AveragePlaceSeries, TenhouRating, TenhouRatingNoAdj, AverageScore, GamesCount, MaxScore, ScoreSum)}


@transaction.atomic()
def process_all_ratings(instance, force=False):
    ratings = instance.rating_set.all()
    if not force:
        ratings = ratings.filter(state=models.Rating.STATE_INQUEUE)
    for rating in ratings:
        rating.stats_set.all().delete()
        logging.info('Processing rating %s', rating)
        rating.state = models.Rating.STATE_COUNTING
        rating.save()
        ALL_RATINGS[rating.rating_type_id](rating, instance.get_backend()).process_and_save()
        rating.state = models.Rating.STATE_ACTUAL
        rating.save()
