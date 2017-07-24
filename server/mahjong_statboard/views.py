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
            'gameresult_set'
        ).all()


class InstancesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Instance.objects.all()
    serializer_class = serializers.InstanceSerializer


class PlayerViewSet(viewsets.ViewSet):
    def list(self, request, instance_pk):
        stats = models.Stats.get_player_stats(instance_id=instance_pk)
        serializer = serializers.PlayerSerializer(stats, many=True)
        return Response(serializer.data)

    def retrieve(self, request, instance_pk, pk):
        stats = models.Stats.get_player_stats(instance_id=instance_pk, player=pk)
        serializer = serializers.PlayerSerializer(stats)
        return Response(serializer.data)
