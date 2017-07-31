import json

from rest_framework import serializers

from mahjong_statboard import models


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


class RatingSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    is_series = serializers.BooleanField(source='get_rating_type.is_series')

    class Meta:
        model = models.Rating
        fields = '__all__'


class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    games = serializers.HyperlinkedIdentityField(view_name='games-list', lookup_url_kwarg='instance_pk')
    players = serializers.HyperlinkedIdentityField(view_name='players-list', lookup_url_kwarg='instance_pk')
    ratings = RatingSerializer(many=True, source='rating_set')

    class Meta:
        model = models.Instance
        fields = '__all__'


class StatsSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = models.Stats
        fields = '__all__'

    def get_value(self, obj):
        return json.loads(obj.value)


class PlayerSerializer(serializers.ModelSerializer):
    stats = StatsSerializer(many=True, read_only=True, source='stats_set')

    class Meta:
        model = models.Player
        fields = '__all__'

