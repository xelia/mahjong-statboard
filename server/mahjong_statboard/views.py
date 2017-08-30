from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, BooleanFilter
from rest_framework import views, viewsets
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mahjong_statboard import models, serializers
from mahjong_statboard.legacy import add_games


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

    @list_route(methods=['post'], permission_classes=(IsAuthenticated,))
    def add_games_legacy(self, request, instance_pk):
        return Response(add_games(request.data['raw_games'], models.Instance.objects.get(pk=instance_pk), request.user))


class ProductFilter(FilterSet):
    active = BooleanFilter(method='active_player_filter')

    class Meta:
        model = models.Player
        fields = ['hidden']

    def active_player_filter(self, queryset, name, value):
        if value:
            return queryset.annotate(games_count=Count('gameresult')).filter(hidden=False, games_count__gte=10)
        else:
            return queryset


class PlayersViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.PlayerSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filter_class = ProductFilter

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


class CurrentUserView(views.APIView):
    def get(self, request):
        print(request.user)
        return Response(serializers.UserSerializer(request.user).data)

