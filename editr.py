import os
import time
import base64
import spotipy
import schedule

from datetime import datetime
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# Constants
SCOPE = 'playlist-modify-public ugc-image-upload'
CACHE_PATH = './cached-token'
PL_COVER_PATH = "cover.png"


def update_playlist():
    load_dotenv()

    username = os.getenv('USERNAME')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')

    pl_id = os.getenv('PLAYLIST_ID')
    pl_title = os.getenv('PLAYLIST_TITLE')
    pl_description = os.getenv('PLAYLIST_DESCRIPTION')

    with open(PL_COVER_PATH, "rb") as png_file:
        pl_cover = base64.b64encode(png_file.read())

    oauth = SpotifyOAuth(username=username,
                         scope=SCOPE,
                         client_id=client_id,
                         client_secret=client_secret,
                         redirect_uri=redirect_uri,
                         cache_path=CACHE_PATH)

    if os.path.isfile(CACHE_PATH):
        token = oauth.get_cached_token()
    else:
        token = oauth.get_access_token()

    sp = spotipy.Spotify(auth=token['access_token'])

    sp.playlist_change_details(playlist_id=pl_id, name=pl_title, description=pl_description)
    sp.playlist_upload_cover_image(playlist_id=pl_id, image_b64=pl_cover)

    print("[%s] %s" % (datetime.now(), "playlist updated"))


if __name__ == "__main__":
    load_dotenv()

    print("[%s] %s" % (datetime.now(), "starting playlist editr ..."))

    update_playlist()
    schedule.every(1).minutes.do(update_playlist)

    while True:
        schedule.run_pending()
        time.sleep(1)  # Delay between executions to avoid high CPU usage
