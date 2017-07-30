from rest_framework import viewsets
from rest_framework.response import Response

from mahjong_statboard import models, serializers


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


class InstancesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Instance.objects.all()
    serializer_class = serializers.InstanceSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PlayerSerializer
    pagination_class = None

    def get_queryset(self):
        return models.Player.objects.filter(
            instance_id=self.kwargs.get('instance_pk')
        ).prefetch_related(
            'stats_set',
        ).all()
