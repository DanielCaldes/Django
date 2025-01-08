from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyAPIView, SpotifyView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    path('spotify/', SpotifyView.as_view(), name='spotify-detail')
]
