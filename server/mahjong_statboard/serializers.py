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
