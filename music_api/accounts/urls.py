from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyAPIView
from .views import FavouriteArtistListCreateDestroyView, FavouriteTrackListCreateDestroyView
from .views import SpotifyArtistView, SpotifyTrackView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    
    path('users/<int:user_id>/favourites/artists/', FavouriteArtistListCreateDestroyView.as_view(), name='artist-favourites-detail'),
    path('users/<int:user_id>/favourites/tracks/', FavouriteTrackListCreateDestroyView.as_view(), name='track-favourites-detail'),
    
    path('spotify/artists/<str:artist_name>', SpotifyArtistView.as_view(), name='spotify-detail'),
    path('spotify/tracks/<str:track_name>', SpotifyTrackView.as_view(), name='spotify-detail'),
    path('spotify/tracks/<str:track_name>/<str:artist_name>', SpotifyTrackView.as_view(), name='spotify-detail')
]
