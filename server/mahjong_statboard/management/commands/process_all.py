# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from mahjong_statboard import models
from mahjong_statboard.models import Rating, Stats
from mahjong_statboard.rating import process_all_ratings


class Command(BaseCommand):
    def handle(self, *args, **options):
        process_all_ratings(instance=models.Instance.objects.first())