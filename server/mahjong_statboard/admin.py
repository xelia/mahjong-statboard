from django.contrib import admin

from . import models


@admin.register(models.Instance)
class InstanceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Stats)
class StatsAdmin(admin.ModelAdmin):
    list_filter = ('rating', )
    list_display = ('instance', 'rating', 'player', 'value', 'game')