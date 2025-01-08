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

class FavouriteTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteTrack
        fields = ['user', 'track_id']