from rest_framework.views import APIView
from rest_framework.response import Response
from .spotify_integration import get_spotify_access_token, get_spotify_tracks
from .models import Track

class SpotifyTracksView(APIView):
    def get(self, request):
        access_token = get_spotify_access_token()
        query = request.query_params.get('q', 'Your search query')
        tracks = get_spotify_tracks(access_token, query)

        for track in tracks:
            Track.objects.create(
                name=track['name'],
                artist=track['artists'][0]['name']
                # Добавьте остальные поля...
            )

        return Response(tracks)
