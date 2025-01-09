import requests
from base64 import b64encode
from django.conf import settings
from typing import List, Optional

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
    
    def search_artist_by_id(self, artist_id : str):
        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            artist = response.json()
            return {
                "id":artist['id'],
                "name":artist['name'],
                "uri":artist['uri']
            }
        else:
            raise None
    
    def search_track_by_name(self, track_name : str, artist_name : Optional[str] = ""):
        url = "https://api.spotify.com/v1/search"

        if artist_name:
            query = f"track:{track_name} artist:{artist_name}"
            limit = 1
        else:
            query = f"track:{track_name}"
            limit = 50
        params = {
            'q': query,
            'type': 'track',
            'limit': limit
        }
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if data['tracks']['items']:
                if limit == 1:
                    track = data['tracks']['items'][0]

                    artists = [{
                        "name":artist['name'],
                        "id":artist['id'],
                        "uri":artist['uri']}
                        for artist in track['artists']]
                    
                    return {
                        "id":track['id'],
                        "name":track['name'],
                        "uri":track['uri'],
                        "artists":artists
                    }
                else:
                    artists_dict = {}
                    tracks = data['tracks']['items']
                    tracks_sorted = sorted(tracks, key=lambda x: x['popularity'], reverse=True)
                    for track in tracks_sorted:
                        for artist in track['artists']:
                            artist_name = artist['name']
                            track_popularity = track['popularity']
                            if artist_name not in artists_dict or track_popularity > artists_dict[artist_name]['track_popularity']:
                                artists_dict[artist_name] = {
                                    'artist_name': artist_name,
                                    'track_popularity': track_popularity
                                    }
                    return [{"artist_name": artist['artist_name'], "track_popularity": artist['track_popularity']}
                            for artist in artists_dict.values()]
            else:
                raise None
        else:
            raise None

    def search_track_by_id(self, track_id : str):
        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            track = response.json()
            
            artists = [{
                "name":artist['name'],
                "id":artist['id'],
                "uri":artist['uri']}
                for artist in track['artists']]
            
            return {
                "id":track['id'],
                "name":track['name'],
                "uri":track['uri'],
                "artists":artists
            }
        else:
            raise None

