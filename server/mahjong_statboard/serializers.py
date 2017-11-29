import json

from rest_framework import serializers

from mahjong_statboard import models


class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    games = serializers.HyperlinkedIdentityField(view_name='games-list', lookup_url_kwarg='instance_pk')
    games_csv = serializers.HyperlinkedIdentityField(view_name='games-csv', lookup_url_kwarg='instance_pk')
    players = serializers.HyperlinkedIdentityField(view_name='players-list', lookup_url_kwarg='instance_pk')
    ratings = serializers.HyperlinkedIdentityField(view_name='ratings-list', lookup_url_kwarg='instance_pk')
    meetings = serializers.HyperlinkedIdentityField(view_name='meetings-list', lookup_url_kwarg='instance_pk')
    # admins = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')

    class Meta:
        model = models.Instance
        exclude = ('pantheon_id', 'admins',)


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


class StatsWithRatingSerializer(StatsSerializer):
    rating = RatingSerializer()


class ExtendedRatingSerializer(RatingSerializer):
    stats = serializers.DictField(child=StatsSerializer())


class PlayerSerializer(serializers.ModelSerializer):
    games_count = serializers.IntegerField(required=False)

    class Meta:
        model = models.Player
        fields = '__all__'


class ExtendedPlayerSerializer(PlayerSerializer):
    stats = StatsWithRatingSerializer(source='stats_set', many=True)


class PlayerNameRelatedField(serializers.SlugRelatedField):
    def __init__(self, **kwargs):
        kwargs['slug_field'] = kwargs.get('slug_field', 'name')
        super().__init__(**kwargs)

    def get_queryset(self):
        return models.Player.objects.filter(instance_id=self.context.get('instance_pk'))


class PlayerMergeSerializer(serializers.Serializer):
    player_to_delete = PlayerNameRelatedField()
    main_player = PlayerNameRelatedField()

    def validate(self, data):
        if data['player_to_delete'] == data['main_player']:
            raise serializers.ValidationError("Players must be different")
        if models.Game.objects.filter(
            gameresult__player=data['main_player']
        ).filter(
            gameresult__player=data['player_to_delete']
        ).count():
            raise serializers.ValidationError('Cannot merge players with shared games')
        return data


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


class OpponentSerializer(serializers.Serializer):
    wins = serializers.IntegerField()
    losses = serializers.IntegerField()
    player = PlayerSerializer()
