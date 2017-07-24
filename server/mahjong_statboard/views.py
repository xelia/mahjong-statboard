from rest_framework import pagination, viewsets

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

