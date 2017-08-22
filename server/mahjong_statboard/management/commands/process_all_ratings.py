# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from mahjong_statboard import models
from mahjong_statboard.models import Rating, Stats
from mahjong_statboard.rating import process_all_ratings


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            default=False,
        )

    def handle(self, *args, **options):
        for instance in models.Instance.objects.all():
            if options['force']:
                instance.rating_set.update(state=models.Rating.STATE_INQUEUE)
            process_all_ratings(instance=instance)