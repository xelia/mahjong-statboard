from rest_framework import pagination, viewsets

from mahjong_statboard import models, serializers


class GamesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Game.objects.order_by('-date', '-addition_time').prefetch_related('gameresult_set').all()
    serializer_class = serializers.GameSerializer
    pagination_class = pagination.PageNumberPagination
