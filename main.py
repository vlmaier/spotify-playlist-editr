import os
import schedule
import spotipy
import base64

from spotipy import SpotifyOAuth
from dotenv import load_dotenv
from datetime import datetime

print("[%s] %s" % (datetime.now(), "starting playlist editr ..."))


def update_playlist():
    load_dotenv()

    username = os.getenv('USERNAME')
    scope = 'playlist-modify-public ugc-image-upload'
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')
    cache_path = './cached-token'

    oauth = SpotifyOAuth(username=username,
                         scope=scope,
                         client_id=client_id,
                         client_secret=client_secret,
                         redirect_uri=redirect_uri,
                         cache_path=cache_path)

    if os.path.isfile(cache_path):
        token = oauth.get_cached_token()
    else:
        token = oauth.get_access_token()

    sp = spotipy.Spotify(auth=token['access_token'])

    pl_id = os.getenv('PLAYLIST_ID')
    pl_title = os.getenv('PLAYLIST_NAME')
    pl_description = os.getenv('PLAYLIST_DESCRIPTION')

    # ideally 300x300 png file
    with open("cover.png", "rb") as png_file:
        pl_cover = base64.b64encode(png_file.read())

    sp.playlist_change_details(playlist_id=pl_id, name=pl_title, description=pl_description)
    sp.playlist_upload_cover_image(playlist_id=pl_id, image_b64=pl_cover)

    print("[%s] %s" % (datetime.now(), "playlist updated"))


update_playlist()
schedule.every(1).minutes.do(update_playlist)

while True:
    schedule.run_pending()
    continue
