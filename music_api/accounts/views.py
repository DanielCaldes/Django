from rest_framework import generics
from .models import User,FavouriteArtist,FavouriteTrack
from .serializers import UserSerializer, FavouriteArtistSerializer, FavouriteTrackSerializer, FavouriteArtistDeleteSerializer, FavouriteTrackDeleteSerializer

from django.http import JsonResponse
from django.views import View
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.spotify import SpotifyAPI

# Genericos para crear y listar usuarios
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#Genericos para actualizar y borrar usuarios
class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#End-point para añadir y borrar los artistas favoritos de un usuario
@method_decorator(csrf_exempt, name='dispatch')
class FavouriteArtistListCreateDestroyView(View):
    def get(self, request, user_id):
        if not user_id:
            return JsonResponse({"error": "No se proporcionó el id del usuario"}, status=400)
        
        favourite_artists = FavouriteArtist.objects.filter(user_id=user_id)
        spotify = SpotifyAPI()

        artists =[]
        for artist in favourite_artists:
            data = spotify.search_artist_by_id(artist.artist_id)
            if data:
                artists.append(data)
            else:
                artist = FavouriteArtist.objects.get(artist_id=artist.artist_id, user_id=user_id)
                artist.delete()
                print("Se ha limpiado un id de usuario invalido")

        return JsonResponse({"favorite_artists": artists}, status=200)
    
    def post(self, request, user_id):
        body = json.loads(request.body)
        artist_id = body.get("artist_id")

        serializer = FavouriteArtistSerializer(data={"user":user_id,"artist_id":artist_id})
        serializer.is_valid(raise_exception=True)

        valid_data = serializer.validated_data
        user_id = valid_data["user"].id
        artist_id = valid_data["artist_id"]
        
        if FavouriteArtist.objects.filter(user_id=user_id, artist_id=artist_id).exists():
            return JsonResponse({"error": "El artista ya está en los favoritos del usuario."}, status=404)
    
        favourite_artists = FavouriteArtist(user_id=user_id, artist_id=artist_id)
        favourite_artists.save()
        return JsonResponse({"message": f"El artista con id {artist_id} ha sido agregado a los favoritos del usuario con id {user_id}."})

    def delete(self, request, user_id):
        body = json.loads(request.body)
        artist_id = body.get("artist_id")
        
        serializer = FavouriteArtistDeleteSerializer(data={"user_id":user_id,"artist_id":artist_id})
        serializer.is_valid(raise_exception=True)

        valid_data = serializer.validated_data
        user_id = valid_data["user_id"]
        artist_id = valid_data["artist_id"]
        
        try:
            artist = FavouriteArtist.objects.get(artist_id=artist_id, user_id=user_id)
        except FavouriteArtist.DoesNotExist:
            return JsonResponse({"error": "No artist with id found for delete"}, status=404)
        
        artist.delete()
        return JsonResponse({"message": "Artist deleted successfully"}, status=200)
        
#End-point para añadir y borrar los artistas favoritos de un usuario
@method_decorator(csrf_exempt, name='dispatch')
class FavouriteTrackListCreateDestroyView(View):
    def get(self, request, user_id):
        if not user_id:
            return JsonResponse({"error": "No se proporcionó el id del usuario"}, status=400)
        
        favourite_tracks = FavouriteTrack.objects.filter(user_id=user_id)
        spotify = SpotifyAPI()

        tracks = [spotify.search_track_by_id(track.track_id) for track in favourite_tracks]
        
        tracks =[]
        for track in favourite_tracks:
            data = spotify.search_track_by_id(track.track_id)
            if data:
                tracks.append(data)
            else:
                invalid_track = FavouriteTrack.objects.get(track_id=track.track_id, user_id=user_id)
                invalid_track.delete()
                print("Se ha limpiado un id de cancion invalido")

        return JsonResponse({"favorite_tracks": tracks}, status=200)
    
    def post(self, request, user_id):
        body = json.loads(request.body)
        track_id = body.get("track_id")

        serializer = FavouriteTrackSerializer(data={"user": user_id, "track_id": track_id})
        serializer.is_valid(raise_exception=True)
        
        valid_data = serializer.validated_data
        user_id = valid_data["user"].id
        track_id = valid_data["track_id"]

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "El usuario no existe"}, status=404)
        
        if FavouriteTrack.objects.filter(user_id=user, track_id=track_id).exists():
            return JsonResponse({"error": "El artista ya está en los favoritos del usuario."}, status=404)
    
        favourite_tracks = FavouriteTrack(user_id=user, track_id=track_id)
        favourite_tracks.save()
        return JsonResponse({"message": f"La canción con id {track_id} ha sido agregado a los favoritos del usuario con id {user_id}."})

    def delete(self, request, user_id):
        body = json.loads(request.body)
        user_id = user_id
        track_id = body.get("track_id")
        
        serializer = FavouriteTrackDeleteSerializer(data={"user_id":user_id,"track_id":track_id})
        serializer.is_valid(raise_exception=True)
        valid_data=serializer.validated_data
        
        user_id = valid_data["user_id"]
        track_id = valid_data["track_id"]

        try:
            artist = FavouriteTrack.objects.get(track_id=track_id, user_id=user_id)
            artist.delete()
            return JsonResponse({"message": "Track deleted successfully"}, status=200)
        except FavouriteTrack.DoesNotExist:
            return JsonResponse({"error": f"No track with id {track_id} found for delete"}, status=404)
  

#End-point para buscar un artista por nombre
@method_decorator(csrf_exempt, name='dispatch')
class SpotifyArtistView(View):
    def get(self, request, artist_name):
        try:
            if not artist_name:
                return JsonResponse({"error": "No se proporcionó el nombre del artista"}, status=400)

            # Inicializar la clase SpotifyAPI
            spotify = SpotifyAPI()

            # Usar la función auxiliar para buscar el artista por nombre
            artist_info = spotify.search_artist_by_name(artist_name)

            if artist_info:
                return JsonResponse({"artist_info": artist_info}, status=200)
            else:
                return JsonResponse({"error": "No se encontró información del artista"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "El cuerpo del mensaje es inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error al procesar la petición: {str(e)}"}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class SpotifyTrackView(View):
    def get(self, request, track_name, artist_name=""):
        try:
            if not track_name:
                return JsonResponse({"error": "No se proporcionó el nombre de la canción"}, status=400)

            # Inicializar la clase SpotifyAPI
            spotify = SpotifyAPI()

            # Usar la función auxiliar para buscar el artista por nombre
            if not artist_name:
                track_info = spotify.search_track_by_name(track_name)
            else:
                track_info = spotify.search_track_by_name(track_name, artist_name)

            if track_info:
                return JsonResponse({"track_info": track_info}, status=200)
            else:
                return JsonResponse({"error": "No se encontró información de la canción"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "El cuerpo del mensaje es inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error al procesar la petición: {str(e)}"}, status=500)
