import time
import os
import base64
import requests
from spotify.models import SpotifyData
from urllib import parse

spotipy_client_id = os.environ.get('spotipy_client_id')
spotipy_client_secret = os.environ.get('spotipy_client_secret')
spotipy_redirect_uri = os.environ.get('spotipy_redirect_uri')


def _make_authorization_headers():
    auth_header = base64.b64encode((spotipy_client_id + ":" + spotipy_client_secret).encode("ascii"))
    return {"Authorization": "Basic %s" % auth_header.decode("ascii")}


def parse_response_code(url):
    try:
        return url.split("?code=")[1].split("&")[0]
    except IndexError:
        return None


def is_token_expired(token_info):
    now = int(time.time())
    return token_info - now < 60


def _get_header(token):
    header = {"Authorization": "Bearer {0}".format(token['access_token'])}
    return header


def get_user(token):
    header = _get_header(token)
    response = requests.get('https://api.spotify.com/v1/me', headers=header)
    items = response.json()
    return items


class Token:
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
    OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"

    def __init__(self, user=None):
        self.scope = 'streaming, user-read-email, user-read-private, user-top-read, user-modify-playback-state, ' \
                     'user-read-playback-state, playlist-read-collaborative, playlist-modify-public, ' \
                     'playlist-read-private, playlist-modify-private, user-library-modify, user-library-read'
        self.token = None
        self.token_info = None
        self.code = None
        self.user = user

    def prompt_for_user_token(self):
        if not self.token_info:
            auth_url = self.get_authorize_url()
            data = {
                "auth_url": auth_url
            }
            return data
        else:
            return self.token_info

    def get_authorize_url(self):
        payload = {
            "client_id": spotipy_client_id,
            "response_type": "code",
            "redirect_uri": spotipy_redirect_uri,
        }
        if self.scope:
            payload["scope"] = self.scope
        urlparams = parse.urlencode(payload)
        return "%s?%s" % (self.OAUTH_AUTHORIZE_URL, urlparams)

    def get_access_token(self, code=None):
        payload = {
            "redirect_uri": spotipy_redirect_uri,
            "code": code,
            "grant_type": "authorization_code",
        }
        if self.scope:
            payload["scope"] = self.scope
        headers = _make_authorization_headers()
        response = requests.post(
            self.OAUTH_TOKEN_URL,
            data=payload,
            headers=headers,
            verify=True,
            timeout=None,
        )
        if response.status_code != 200:
            return response
        token_info = response.json()
        token_info = self._add_custom_values_to_token_info(token_info)
        user_id = get_user(token_info)
        try:
            obj, created = SpotifyData.objects.get_or_create(user=self.user, sp_name=user_id.get('id'),
                                              access_token=token_info['access_token'],
                                              refresh_token=token_info['refresh_token'],
                                              expires_at=token_info['expires_at'],
                                              category=user_id.get('product'))
            print(obj, created)
        except Exception as e:
            print(e)
        token_info['user'] = user_id
        token_info['status_code'] = response.status_code
        return token_info

    def _add_custom_values_to_token_info(self, token_info):
        token_info["expires_at"] = (int(time.time()) + token_info["expires_in"])*1000
        token_info["scope"] = self.scope
        return token_info

    def refresh_access_token(self):
        data = SpotifyData.objects.get(user=self.user)
        refresh_token = data.refresh_token
        payload = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
        headers = _make_authorization_headers()
        response = requests.post(
            self.OAUTH_TOKEN_URL,
            data=payload,
            headers=headers,
            proxies=None,
            timeout=None,
        )
        if response.status_code != 200:
            return response
        token_info = response.json()
        token_info = self._add_custom_values_to_token_info(token_info)
        token_info['status_code'] = response.status_code
        if "refresh_token" not in token_info:
            token_info["refresh_token"] = refresh_token
        data.access_token = token_info['access_token']
        data.refresh_token = token_info['refresh_token']
        data.expires_at = token_info['expires_at']
        data.save()
        return token_info
