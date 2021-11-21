from rest_framework.serializers import ModelSerializer
from .models import Configuration
from django.contrib.auth import get_user_model
from webapp.models import Movie,Genre,Season,Episode,WatchEpisode,WatchMovie,Report,Cast
class ConfigSerializer(ModelSerializer):
    class Meta:
        model = Configuration
        fields = "__all__"
class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movie
        exclude = ("slug",)
class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name",)
class SeasonSerializer(ModelSerializer):
    class Meta:
        model = Season
        exclude = ("episode_count",)
class EpisodeSerializer(ModelSerializer):
    class Meta:
        model = Episode
        exclude = ("slug",)
class WatchEpisodeSerializer(ModelSerializer):
    class Meta:
        model = WatchEpisode
        fields = "__all__"
class WatchMovieSerializer(ModelSerializer):
    class Meta:
        model  = WatchMovie
        fields = "__all__"
class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username","email","password")
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"
class CastSerializer(ModelSerializer):
    class Meta:
        model = Cast
        fields = ("id","gender","name","tmdb_cast_id","profile_path","added_on",)