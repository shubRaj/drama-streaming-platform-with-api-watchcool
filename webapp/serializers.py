from rest_framework.serializers import ModelSerializer
from .models import TV
class TVSerializer(ModelSerializer):
    class Meta:
        model = TV
        fields = ("id","title","poster_path","slug")