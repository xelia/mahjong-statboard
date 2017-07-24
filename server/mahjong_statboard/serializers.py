from rest_framework import serializers

from mahjong_statboard import models


class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GameResult
        fields = ('player', 'score', 'place', 'starting_position')


class GameSerializer(serializers.ModelSerializer):
    results = GameResultSerializer(source='gameresult_set', many=True)

    class Meta:
        model = models.Game
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rating
        fields = '__all__'


class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    games = serializers.HyperlinkedIdentityField(view_name='games-list', lookup_url_kwarg='instance_pk')
    ratings = RatingSerializer(many=True, source='rating_set')

    class Meta:
        model = models.Instance
        fields = '__all__'


class PlayerSerializer(serializers.Serializer):
    player = serializers.ReadOnlyField()
    stats = serializers.DictField(read_only=True)

