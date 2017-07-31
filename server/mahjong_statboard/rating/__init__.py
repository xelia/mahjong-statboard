import logging

from django.db import transaction

from mahjong_statboard.rating.backends import LocalBackend
from mahjong_statboard.rating.basic import AveragePlace, AbstractRating
from mahjong_statboard.rating.series import AveragePlaceSeries
from mahjong_statboard.rating.tenhou import TenhouRating

ALL_RATINGS = {r.id: r for r in (AveragePlace, AveragePlaceSeries, TenhouRating)}


@transaction.atomic()
def process_all_ratings(instance):
    backend = LocalBackend(instance)
    for rating in instance.rating_set.all():
        rating.stats_set.all().delete()
        logging.debug('Processing rating %s', rating)
        ALL_RATINGS[rating.rating_type_id](rating, backend).process_and_save()
