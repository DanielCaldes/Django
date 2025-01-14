from rest_framework import serializers
from .models import User, FavouriteArtist, FavouriteTrack

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class FavouriteArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteArtist
        fields = ['user', 'artist_id']

class FavouriteArtistDeleteSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    artist_id = serializers.CharField()

class FavouriteTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteTrack
        fields = ['user', 'track_id']

class FavouriteTrackDeleteSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    track_id = serializers.CharField()
