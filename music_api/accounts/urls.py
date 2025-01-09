from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyAPIView
from .views import FavouriteArtistListCreateDestroyView, FavouriteTrackListCreateDestroyView
from .views import SpotifyArtistView, SpotifyTrackView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    
    path('users/<int:user_id>/favourite/artist/', FavouriteArtistListCreateDestroyView.as_view(), name='artist-favourites-detail'),
    path('users/<int:user_id>/favourite/track/', FavouriteTrackListCreateDestroyView.as_view(), name='track-favourites-detail'),
    
    path('spotify/artist/', SpotifyArtistView.as_view(), name='spotify-detail'),
    path('spotify/track/', SpotifyTrackView.as_view(), name='spotify-detail')
]
