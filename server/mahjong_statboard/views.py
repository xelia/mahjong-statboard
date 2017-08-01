from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from mahjong_statboard import models, serializers


class InstancesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Instance.objects.all()
    serializer_class = serializers.InstanceSerializer


class GamesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.GameSerializer

    def get_queryset(self):
        return models.Game.objects.filter(
            instance_id=self.kwargs.get('instance_pk')
        ).order_by(
            '-date', '-addition_time'
        ).prefetch_related(
            'gameresult_set',
            'gameresult_set__player'
        ).all()


class PlayersViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PlayerSerializer
    pagination_class = None

    def get_serializer_class(self):
        if self.request.GET.get('stats'):
            return serializers.ExtendedPlayerSerializer
        else:
            return serializers.PlayerSerializer

    def get_queryset(self):
        return models.Player.objects.filter(
            instance_id=self.kwargs.get('instance_pk')
        ).prefetch_related(
            'stats_set',
        ).all()


class RatingsViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None

    def get_serializer_class(self):
        if self.request.GET.get('stats'):
            return serializers.ExtendedRatingSerializer
        else:
            return serializers.RatingSerializer

    def get_queryset(self):
        return models.Rating.objects.filter(
            instance_id=self.kwargs.get('instance_pk')
        ).prefetch_related(
            'stats_set',
        ).all()


class StatsViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = serializers.StatsSerializer
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('player', 'rating',)

    def get_queryset(self):
        return models.Stats.objects.filter(
            rating__instance_id=self.kwargs.get('instance_pk')
        ).all()