from rest_framework import serializers
from .models import User, FavouriteArtist, FavouriteTrack

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class FavouriteArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteArtist
        fields = ['user', 'spotify_artist_id']

class FavouriteArtistDeleteSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    spotify_artist_id = serializers.CharField()

class FavouriteTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteTrack
        fields = ['user', 'spotify_track_id']

class FavouriteTrackDeleteSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    spotify_track_id = serializers.CharField()
