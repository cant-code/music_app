import json

import requests
import os
from spotify.models import SpotifyData

spotipy_client_id = os.environ.get('spotipy_client_id')
spotipy_client_secret = os.environ.get('spotipy_client_secret')
spotipy_redirect_uri = os.environ.get('spotipy_redirect_uri')


def _get_header(token):
    header = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token)
    }
    return header


class Playback:
    API_URl = 'https://api.spotify.com/v1/'

    def __init__(self, user=None):
        self.user = user

    def start_playback(self, device=None, context_uri=None, uris=None, offset=None, position_ms=None):
        data = {}
        params = {'device_id': device}
        userData = SpotifyData.objects.get(user=self.user)
        access_token = userData.access_token
        data['context_uri'] = 'spotify:album:6ZG5lRT77aJ3btmArcykra'
        data['position_ms'] = 0
        if context_uri is not None:
            data["context_uri"] = context_uri
        if uris is not None:
            data["uris"] = uris
        if offset is not None:
            data["offset"] = offset
        if position_ms is not None:
            data["position_ms"] = position_ms
        url = self.API_URl + 'me/player/play?device_id='+device
        json_data = json.dumps(data)
        headers = _get_header(access_token)
        requests.put(url, data=json_data, headers=headers, proxies=None, timeout=None)

    def pause_playback(self):
        userData = SpotifyData.objects.get(user=self.user)
        access_token = userData.access_token
        url = self.API_URl + 'me/player/pause'
        headers = _get_header(access_token)
        response = requests.put(url, data=None, headers=headers, proxies=None, timeout=None)
        print(response.status_code)
