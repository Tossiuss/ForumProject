import requests
from django.conf import settings

def get_spotify_access_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(auth_url, data=payload)
    data = response.json()
    return data.get('access_token')

def get_spotify_tracks(access_token, query):
    api_url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'q': query, 'type': 'track', 'limit': 10}
    response = requests.get(api_url, headers=headers, params=params)
    data = response.json()
    tracks = data.get('tracks', {}).get('items', [])
    return tracks
