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

    def spotify_request(self, endpoint: str, params: Optional[dict] = None):
        """Make a request to the Spotify API and handle the access token."""
        url = f"https://api.spotify.com/v1/{endpoint}"
        
        headers = { 'Authorization': f'Bearer {self.access_token}' }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("The token has expired, obtaining a new one...")
            self.access_token = self.get_spotify_token()
            headers = { 'Authorization': f'Bearer {self.access_token}' }
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(status_code=response.status_code, detail=f"Error in the request after refreshing the token: {response.status_code}, {response.text}")
        else:
            raise Exception({"status_code": response.status_code, "detail": f"Error in the request: {response.status_code}, {response.text}"})

    def search_artist_by_name(self, artist_name):
        params = {'q': artist_name, 'type': 'artist', 'limit': 1}

        data = self.spotify_request("search",params)

        if not data or 'artists' not in data or 'items' not in data['artists'] or not data['artists']['items']:
            raise Exception(status_code=404, detail="No artist was found with that name.")

        artist = data['artists']['items'][0]
        return {
            "id" : artist['id'],
            "name" : artist['name'],
            "uri" : artist['uri']
        }
    
    def search_artist_by_id(self, artist_id : str):
        artist = self.spotify_request(f"artists/{artist_id}")
        
        if artist:
            return {
                "id":artist['id'],
                "name":artist['name'],
                "uri":artist['uri']
            }
        else:
            return None
    
    def search_track_by_name(self, track_name : str, artist_name : Optional[str] = ""):
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
        
        data = self.spotify_request("search", params)

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
            return None

    def search_track_by_id(self, track_id : str):
        track_data = self.spotify_request(f"tracks/{track_id}")
        
        if track_data:
            artists = [{
                "name":artist['name'],
                "id":artist['id'],
                "uri":artist['uri']}
                for artist in track_data['artists']]
            
            return {
                "id":track_data['id'],
                "name":track_data['name'],
                "uri":track_data['uri'],
                "artists":artists
            }
        else:
            return None

