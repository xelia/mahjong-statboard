import json

from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from mahjong_statboard import models


class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    games = serializers.HyperlinkedIdentityField(view_name='games-list', lookup_url_kwarg='instance_pk')
    players = serializers.HyperlinkedIdentityField(view_name='players-list', lookup_url_kwarg='instance_pk')
    ratings = serializers.HyperlinkedIdentityField(view_name='ratings-list', lookup_url_kwarg='instance_pk')
    meetings = serializers.HyperlinkedIdentityField(view_name='meetings-list', lookup_url_kwarg='instance_pk')

    class Meta:
        model = models.Instance
        fields = '__all__'


class GameResultSerializer(serializers.ModelSerializer):
    player = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = models.GameResult
        fields = ('player', 'score', 'place', 'starting_position')


class GameSerializer(serializers.ModelSerializer):
    results = GameResultSerializer(source='gameresult_set', many=True)

    class Meta:
        model = models.Game
        fields = '__all__'


class StatsSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = models.Stats
        fields = '__all__'

    def get_value(self, obj):
        return json.loads(obj.value)


class RatingSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    is_series = serializers.BooleanField(source='get_rating_type.is_series')

    class Meta:
        model = models.Rating
        fields = '__all__'


class ExtendedRatingSerializer(RatingSerializer):
    stats = serializers.DictField(child=StatsSerializer())


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Player
        fields = '__all__'


class ExtendedPlayerSerializer(PlayerSerializer):
    stats = serializers.DictField(child=StatsSerializer())


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    is_authenticated = serializers.BooleanField()


class MeetingSerializer(serializers.Serializer):
    date = serializers.DateField()
    players = serializers.SerializerMethodField()
    games_count = serializers.IntegerField()
    players_count = serializers.SerializerMethodField()

    def get_players(self, obj):
        return obj['players'].split(';')

    def get_players_count(self, obj):
        return len(obj['players'].split(';'))
