from rest_framework import generics
from .models import User
from .serializers import UserSerializer

from django.http import JsonResponse
from django.views import View
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from utils.spotify import SpotifyAPI

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@method_decorator(csrf_exempt, name='dispatch')
class SpotifyView(View):
    def post(self, request):
        try:
            # Leer y parsear el cuerpo del mensaje
            body = json.loads(request.body)
            user_artist_name = body.get("artist_name")

            if not user_artist_name:
                return JsonResponse({"error": "No se proporcionó el nombre del artista"}, status=400)

            # Inicializar la clase SpotifyAPI
            spotify = SpotifyAPI()

            # Usar la función auxiliar para buscar el artista por nombre
            artist_info = spotify.search_artist_by_name(user_artist_name)

            if artist_info:
                return JsonResponse({"artist_info": artist_info}, status=200)
            else:
                return JsonResponse({"error": "No se encontró información del artista"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"error": "El cuerpo del mensaje es inválido"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Error al procesar la petición: {str(e)}"}, status=500)