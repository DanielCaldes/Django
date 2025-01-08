import requests
from base64 import b64encode
from django.conf import settings

class SpotifyAPI:
    def __init__(self):
        self.client_id = settings.SPOTIFY_CLIENT_ID
        self.client_secret = settings.SPOTIFY_CLIENT_SECRET
        self.access_token = self.get_spotify_token()

    def get_spotify_token(self):
        url = "https://accounts.spotify.com/api/token"
        credentials = b64encode(f"{self.client_id}:{self.client_secret}".encode('utf-8')).decode('utf-8')
        headers = {"Authorization": f"Basic {credentials}"}
        data = {"grant_type": "client_credentials"}

        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            raise Exception(f"Failed to obtain Spotify token: {response.status_code}")

    def search_artist_by_name(self, artist_name):
        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {'q': artist_name, 'type': 'artist', 'limit': 1}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['artists']['items']:
                artist = data['artists']['items'][0]
                return {
                    "name": artist['name'],
                    "id": artist['id'],
                    "uri": artist['uri']
                }
        return None