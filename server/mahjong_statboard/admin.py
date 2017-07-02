from django.contrib import admin

from . import models


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Stats)
class StatsAdmin(admin.ModelAdmin):
    pass