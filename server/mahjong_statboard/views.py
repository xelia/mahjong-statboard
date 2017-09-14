from django.contrib.postgres.aggregates.general import StringAgg
from django.db.models.aggregates import Count
from django.http.response import HttpResponse
from django.views.generic.base import View
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, BooleanFilter, CharFilter
from rest_framework import views, viewsets, mixins
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mahjong_statboard import models, serializers
from mahjong_statboard.legacy import add_games


class InstancesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Instance.objects.all()
    serializer_class = serializers.InstanceSerializer


class GameFilter(FilterSet):
    player = CharFilter(name='gameresult__player__name', label='Player')

    class Meta:
        model = models.Game
        fields = ('player', )


class GamesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.GameSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = GameFilter

    def get_queryset(self):
        return models.Game.objects.filter(
            instance_id=self.kwargs.get('instance_pk')
        ).order_by(
            '-date', '-addition_time'
        ).prefetch_related(
            'gameresult_set',
            'gameresult_set__player'
        ).all()

    @property
    def paginator(self):
        if self.request.query_params.get('player'):
            return None
        return super().paginator

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

    @detail_route()
    def opponents(self, request, instance_pk, pk):
        return Response(serializers.OpponentSerializer(self.get_object().opponents, many=True).data)

    def get_serializer_class(self):
        if self.request.GET.get('extended'):
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


class MeetingsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.MeetingSerializer

    def get_queryset(self):
        return models.Game.objects.filter(
            instance_id=self.kwargs['instance_pk']
        ).values(
            'date'
        ).annotate(
            players=StringAgg('gameresult__player__name', ';', distinct=True),
            games_count=Count('id', distinct=True),
        ).order_by('-date')


class GamesListCsv(View):
    def get(self, request, instance_pk):
        games = models.Game.objects.filter(instance_id=instance_pk).prefetch_related('gameresult_set', 'gameresult_set__player')
        result = ''
        for game in games:
            line = [game.date.strftime('%d.%m.%Y')]
            for game_result in game.gameresult_set.all():
                line.append(game_result.player.name)
                line.append(str(game_result.score))
            result += ';'.join(line) + '\n'
        return HttpResponse(result, content_type='text/csv')
