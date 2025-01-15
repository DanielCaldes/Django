#Generics
from rest_framework import generics

#Json
from django.http import JsonResponse
import json

#Decorator for custom endpoints to avoid security error
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#Custom class modules
from .models import User,FavouriteArtist,FavouriteTrack
from .serializers import UserSerializer, FavouriteArtistSerializer, FavouriteTrackSerializer, FavouriteArtistDeleteSerializer, FavouriteTrackDeleteSerializer
from utils.spotify import SpotifyAPI

#Swagger
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# Generics to Create and List Users
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Generics to Update and Delete Users
class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Endpoint to Add and Delete a User's Favorite Artists
@method_decorator(csrf_exempt, name='dispatch')
class FavouriteArtistListCreateDestroyView(APIView):
    @swagger_auto_schema(
        operation_description="Get a user's favorite artists",
        responses={
            200: openapi.Response(
                description="List of favorite songs",
                examples={
                    "json":{
                        "favorite_artists": [
                            {
                            "id": "1EXjXQpDx2pROygh8zvHs4",
                            "name": "Melendi",
                            "uri": "spotify:artist:1EXjXQpDx2pROygh8zvHs4"
                            },
                            {
                            "id": "5BMgsAFg8rZQc3tqs5BB8G",
                            "name": "Mecano",
                            "uri": "spotify:artist:5BMgsAFg8rZQc3tqs5BB8G"
                            }
                        ]
                    }
                }
            )
        },
        tags=["favourites"]
    )
    def get(self, request, user_id):
        favourite_artists = FavouriteArtist.objects.filter(user_id=user_id)
        spotify = SpotifyAPI()

        artists =[]
        for artist in favourite_artists:
            try:
                data = spotify.search_artist_by_id(artist.spotify_artist_id)              
                if data:
                    artists.append(data)
            except Exception as e:
                # Check for an Invalid ID, in Which Case Remove It from Favorites
                if e.args[0].get('status_code') == 400:
                    artist = FavouriteArtist.objects.get(artist_id=artist.spotify_artist_id, user_id=user_id)
                    artist.delete()
                    print(f"The invalid id has been cleared {artist.spotify_artist_id}")

        return JsonResponse({"favorite_artists": artists}, status=200)
    
    @swagger_auto_schema(
        operation_description="Add an artist to a user's favorites",
        request_body=FavouriteArtistSerializer,
        responses={
            200: "The artist with id {spotify_artist_id} has been added to the favorites of the user with id {user_id}"
        },
        tags=["favourites"]
    )
    def post(self, request, user_id):
        body = json.loads(request.body)
        spotify_artist_id = body.get("spotify_artist_id")

        serializer = FavouriteArtistSerializer(data={"user":user_id,"spotify_artist_id":spotify_artist_id})
        serializer.is_valid(raise_exception=True)

        valid_data = serializer.validated_data
        user_id = valid_data["user"].id
        spotify_artist_id = valid_data["spotify_artist_id"]
    
        favourite_artists = FavouriteArtist(user_id=user_id, spotify_artist_id=spotify_artist_id)
        favourite_artists.save()
        return JsonResponse({"message": f"The artist with id {spotify_artist_id} has been added to the favorites of the user with id {user_id}"})

    @swagger_auto_schema(
        operation_description="Remove an artist from a user's favorites",
        request_body=FavouriteArtistDeleteSerializer,
        responses={
            200: 'Artist preference removed!',
            404: 'The artist with the provided ID was not found'
        },
        tags=["favourites"]
    )
    def delete(self, request, user_id):
        body = json.loads(request.body)
        spotify_artist_id = body.get("spotify_artist_id")
        
        serializer = FavouriteArtistDeleteSerializer(data={"user_id":user_id,"spotify_artist_id":spotify_artist_id})
        serializer.is_valid(raise_exception=True)

        valid_data = serializer.validated_data
        user_id = valid_data["user_id"]
        spotify_artist_id = valid_data["spotify_artist_id"]
        
        try:
            artist = FavouriteArtist.objects.get(spotify_artist_id=spotify_artist_id, user_id=user_id)
        except FavouriteArtist.DoesNotExist:
            return JsonResponse({"error": "The artist with the provided ID was not found"}, status=404)
        
        artist.delete()
        return JsonResponse({"message": "Artist preference removed!"}, status=200)
        
# Endpoint to Add and Remove a User's Favorite Artists
@method_decorator(csrf_exempt, name='dispatch')
class FavouriteTrackListCreateDestroyView(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of a user's favorite songs by their ID",
        responses={
            200: openapi.Response(
                description="List of favorite tracks",
                examples={
                    "json":{
                        "favorite_tracks": [
                            {
                                "name": "Cut To The Feeling",
                                "id": "11dFghVXANMlKmJXsNCbNl",
                                "uri": "spotify:track:11dFghVXANMlKmJXsNCbNl"
                            }
                        ]
                    }
                }
            )
        },
        tags=["favourites"]
    )
    def get(self, request, user_id):
        favourite_tracks = FavouriteTrack.objects.filter(user_id=user_id)
        spotify = SpotifyAPI()

        tracks = [spotify.search_track_by_id(track.spotify_track_id) for track in favourite_tracks]
        
        tracks =[]
        for track in favourite_tracks:
            try:
                data = spotify.search_track_by_id(track.spotify_track_id)
                if data:
                    tracks.append(data)
            except Exception as e:
                 # Check for an incorrect ID; in that case, remove the ID from favorites
                if e.args[0].get('status_code') == 400:
                    data = None
                    invalid_track = FavouriteTrack.objects.get(spotify_track_id=track.spotify_track_id, user_id=user_id)
                    invalid_track.delete()
                    print(f"The incorrect ID has been cleared {track.spotify_track_id}")

        return JsonResponse({"favorite_tracks": tracks}, status=200)
    
    @swagger_auto_schema(
        operation_description="Add a song to a user's favorites",
        request_body=FavouriteTrackSerializer,
        responses={
            201: "The track with id {spotify_track_id} has been added to the favourites of the user with id {user_id}."
        },
        tags=["favourites"]
    )
    def post(self, request, user_id):
        body = json.loads(request.body)
        spotify_track_id = body.get("spotify_track_id")

        serializer = FavouriteTrackSerializer(data={"user": user_id, "spotify_track_id": spotify_track_id})
        serializer.is_valid(raise_exception=True)
        
        valid_data = serializer.validated_data
        user_id = valid_data["user"].id
        spotify_track_id = valid_data["spotify_track_id"]
    
        favourite_tracks = FavouriteTrack(user_id=user_id, spotify_track_id=spotify_track_id)
        favourite_tracks.save()
        return JsonResponse({"message": f"The track with id {spotify_track_id} has been added to the favourites of the user with id {user_id}."})

    @swagger_auto_schema(
        operation_description="Remove a track from a user's favorites",
        request_body=FavouriteTrackDeleteSerializer,
        responses={
            200: "Track deleted successfully",
            404: "No track with id {track_id} found for delete"
        },
        tags=["favourites"]
    )
    def delete(self, request, user_id):
        body = json.loads(request.body)
        user_id = user_id
        spotify_track_id = body.get("spotify_track_id")
        
        serializer = FavouriteTrackDeleteSerializer(data={"user_id":user_id,"spotify_track_id":spotify_track_id})
        serializer.is_valid(raise_exception=True)
        valid_data=serializer.validated_data
        
        user_id = valid_data["user_id"]
        spotify_track_id = valid_data["spotify_track_id"]

        try:
            artist = FavouriteTrack.objects.get(spotify_track_id=spotify_track_id, user_id=user_id)
            artist.delete()
            return JsonResponse({"message": "Track preference removed!"}, status=200)
        except FavouriteTrack.DoesNotExist:
            return JsonResponse({"error": f"No track with id {spotify_track_id} found for delete"}, status=404)
  

# Endpoint to Search for an Artist by Name
@method_decorator(csrf_exempt, name='dispatch')
class SpotifyArtistView(APIView):
    def get(self, request, artist_name):
        try:
            spotify = SpotifyAPI()
            artist_info = spotify.search_artist_by_name(artist_name)

            if artist_info:
                return JsonResponse({"artist_info": artist_info}, status=200)
            else:
                return JsonResponse({"error": "Artist information not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": f"Error processing the request: {str(e)}"}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class SpotifyTrackView(APIView):
    def get(self, request, track_name, artist_name=""):
        try:
            spotify = SpotifyAPI()
            if not artist_name:
                track_info = spotify.search_track_by_name(track_name)
            else:
                track_info = spotify.search_track_by_name(track_name, artist_name)

            if track_info:
                return JsonResponse({"track_info": track_info}, status=200)
            else:
                return JsonResponse({"error": "Track information not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": f"Error processing the request: {str(e)}"}, status=500)
