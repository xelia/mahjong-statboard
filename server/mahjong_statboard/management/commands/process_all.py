# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from mahjong_statboard.models import Rating


class Command(BaseCommand):
    def handle(self, *args, **options):
        for rating in Rating.objects.all():
            print('Process rating {}'.format(rating))
            rating.process()