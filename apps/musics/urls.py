from django.urls import path
from .views import SpotifyTracksView

urlpatterns = [
    path('spotify-tracks/', SpotifyTracksView.as_view(), name='spotify-tracks'),
]
