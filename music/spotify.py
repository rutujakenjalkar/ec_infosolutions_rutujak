
import base64
import os
import requests

class SpotifyService:
    @staticmethod
    def get_token():
        auth_url = "https://accounts.spotify.com/api/token"
        client_id = os.environ.get('SPOTIFY_CLIENT_ID')
        client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

        if not client_id or not client_secret:
            return None

        auth_str = f"{client_id}:{client_secret}"
        b64_auth_str = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {b64_auth_str}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(auth_url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None

    @staticmethod
    def get_recommendations(genres, limit=10):
        token = SpotifyService.get_token()
        selected_genre = genres[0] if genres and len(genres) > 0 else "pop"

        if not token:
            print("--- SPOTIFY API ERROR: Failed to obtain access token ---")
            return []

        headers = {"Authorization": f"Bearer {token}"}
        search_url = "https://api.spotify.com/v1/search"
        search_params = {
            "q": f"genre:{selected_genre}",
            "type": "track",
            "limit": limit
        }

        response = requests.get(search_url, headers=headers, params=search_params)

        if response.status_code == 200:
            tracks = response.json().get("tracks", {}).get("items", [])
            return [
                {
                    "name": track["name"],
                    "artist": track["artists"][0]["name"],
                    "preview_url": track.get("preview_url"),
                    "spotify_url": track["external_urls"]["spotify"]
                }
                for track in tracks
            ]
        
        print(f"--- SPOTIFY API ERROR ({response.status_code}): {response.text} ---")
        return []