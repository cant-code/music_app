import requests
import os

spotipy_client_id = os.environ.get('spotipy_client_id')
spotipy_client_secret = os.environ.get('spotipy_client_secret')
spotipy_redirect_uri = os.environ.get('spotipy_redirect_uri')


def _get_header(token):
    header = {"Authorization": "Bearer {0}".format(token['access_token'])}
    return header


class Playback:
    API_URl = 'https://api.spotify.com/v1/'

    def start_playback(self, access_token=None, context_uri=None, uris=None, offset=None, position_ms=None):
        data = {}
        if context_uri is not None:
            data["context_uri"] = context_uri
        if uris is not None:
            data["uris"] = uris
        if offset is not None:
            data["offset"] = offset
        if position_ms is not None:
            data["position_ms"] = position_ms
        url = self.API_URl + 'me/player/play'
        headers = _get_header(access_token)
        response = requests.put(url, data=data, headers=headers, proxies=None, timeout=None)
        print(response)

    def pause_playback(self, access_token=None):
        url = self.API_URl + 'me/player/pause'
        headers = _get_header(access_token)
        response = requests.put(url, data=None, headers=headers, proxies=None, timeout=None)
        print(response)
