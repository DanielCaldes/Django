from rest_framework import generics
from .models import User,FavouriteArtist,FavouriteTrack
from .serializers import UserSerializer, FavouriteArtistSerializer, FavouriteTrackSerializer

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

        artists = [spotify.search_artist_by_id(artist.artist_id) for artist in favourite_artists]

        return JsonResponse({"favorite_artists": artists}, status=200)
    
    def post(self, request, user_id):
        body = json.loads(request.body)
        read_artist_id = body.get("artist_id")

        if not user_id:
            return JsonResponse({"error": "No se proporcionó el id del usuario"}, status=400)
        
        if not read_artist_id:
            return JsonResponse({"error": "No se proporcionó el id del artista"}, status=400)

        try:
            user = User.objects.get(id=user_id)
            if FavouriteArtist.objects.filter(user_id=user, artist_id=read_artist_id).exists():
                return JsonResponse({"error": "El artista ya está en los favoritos del usuario."}, status=404)
        
            favourite_artists = FavouriteArtist(user_id=user, artist_id=read_artist_id)
            favourite_artists.save()
            return JsonResponse({"message": f"El artista con id {read_artist_id} ha sido agregado a los favoritos del usuario con id {user_id}."})

        except User.DoesNotExist:
            return JsonResponse({"error": "El usuario no existe"}, status=404)

    def delete(self, request, user_id):
        body = json.loads(request.body)
        artist_id = body.get("artist_id")
        
        if not user_id:
            return JsonResponse({"error": "User ID is required"}, status=400)
        
        if not artist_id:
            return JsonResponse({"error": "Artist ID is required"}, status=400)
        
        try:
            artist = FavouriteArtist.objects.get(artist_id=artist_id, user_id=user_id)
            artist.delete()
            return JsonResponse({"message": "Artist deleted successfully"}, status=200)
        except FavouriteArtist.DoesNotExist:
            return JsonResponse({"error": "No artist with id found for delete"}, status=404)
        
#End-point para añadir y borrar los artistas favoritos de un usuario
@method_decorator(csrf_exempt, name='dispatch')
class FavouriteTrackListCreateDestroyView(View):
    def get(self, request, user_id):
        if not user_id:
            return JsonResponse({"error": "No se proporcionó el id del usuario"}, status=400)
        favourite_tracks = FavouriteTrack.objects.filter(user_id=user_id)
        spotify = SpotifyAPI()

        tracks = [spotify.search_track_by_id(track.track_id) for track in favourite_tracks]

        return JsonResponse({"favorite_tracks": tracks}, status=200)
    
    def post(self, request, user_id):
        body = json.loads(request.body)
        read_user_id = user_id
        read_track_id = body.get("track_id")

        if not read_user_id:
            return JsonResponse({"error": "No se proporcionó el id del usuario"}, status=400)
        
        if not read_track_id:
            return JsonResponse({"error": "No se proporcionó el id de la canción"}, status=400)

        try:
            user = User.objects.get(id=read_user_id)
            if FavouriteTrack.objects.filter(user_id=user, track_id=read_track_id).exists():
                return JsonResponse({"error": "El artista ya está en los favoritos del usuario."}, status=404)
        
            favourite_tracks = FavouriteTrack(user_id=user, track_id=read_track_id)
            favourite_tracks.save()
            return JsonResponse({"message": f"La canción con id {read_track_id} ha sido agregado a los favoritos del usuario con id {read_user_id}."})

        except User.DoesNotExist:
            return JsonResponse({"error": "El usuario no existe"}, status=404)

    def delete(self, request, user_id):
        body = json.loads(request.body)
        user_id = user_id
        track_id = body.get("track_id")
        
        if not user_id:
            return JsonResponse({"error": "User ID is required"}, status=400)
        
        if not track_id:
            return JsonResponse({"error": "Track ID is required"}, status=400)
        
        try:
            artist = FavouriteTrack.objects.get(track_id=track_id, user_id=user_id)
            artist.delete()
            return JsonResponse({"message": "Track deleted successfully"}, status=200)
        except FavouriteTrack.DoesNotExist:
            return JsonResponse({"error": f"No track with id {track_id} found for delete"}, status=404)
  

#End-point para buscar un artista por nombre
@method_decorator(csrf_exempt, name='dispatch')
class SpotifyArtistView(View):
    def post(self, request):
        try:
            # Leer y parsear el cuerpo del mensaje
            body = json.loads(request.body)
            artist_name = body.get("artist_name")

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
    def post(self, request):
        try:
            # Leer y parsear el cuerpo del mensaje
            body = json.loads(request.body)
            track_name = body.get("track_name")
            artist_name = body.get("artist_name")

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
