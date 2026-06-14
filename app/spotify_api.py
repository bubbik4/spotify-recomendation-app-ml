import os
import spotipy
from spotipy.oatuh2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

    if not client_id or not client_secret:
        return None

    # authorizing at Spotify
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(auth_manager=auth_manager)

def get_track_details(track_id):
    sp = get_spotify_client()
    if not sp:
        return None, None

    try:
        track_info = sp.track(track_id)

        images = track_info['album'].get('images', [])
        cover_url = images[0]['url'] if images else None
        
        preview_url = track_info.get('prewiev_url')

        return cover_url, preview_url
    except Exception as e:
        print(f"Błąd API: {e}")
        return None, None