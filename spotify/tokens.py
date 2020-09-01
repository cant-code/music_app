import time
import spotipy.oauth2 as oauth2
import os
import base64
import six
import requests
from spotify.models import SpotifyData

spotipy_client_id = os.environ.get('spotipy_client_id')
spotipy_client_secret = os.environ.get('spotipy_client_secret')
spotipy_redirect_uri = os.environ.get('spotipy_redirect_uri')


def authenticate(user, response):
    code = parse_response_code(response)
    token = Token()
    token.get_access_token(user=user, code=code)


def _make_authorization_headers(client_id, client_secret):
    auth_header = base64.b64encode(six.text_type(client_id + ":" + client_secret).encode("ascii"))
    return {"Authorization": "Basic %s" % auth_header.decode("ascii")}


def parse_response_code(url):
    try:
        return url.split("?code=")[1].split("&")[0]
    except IndexError:
        return None


def is_token_expired(token_info):
    now = int(time.time())
    return token_info - now < 60


def _save_token_info(user, token_info, user_id):
    success = SpotifyData.objects.get_or_create(user=user, sp_name=user_id, access_token=token_info['access_token'],
                                                token_type=token_info['token_type'],
                                                expires_in=token_info['expires_in'],
                                                refresh_token=token_info['refresh_token'],
                                                expires_at=token_info['expires_at'])
    if success:
        print('success')


def _get_header(token):
    header = {"Authorization": "Bearer {0}".format(token['access_token'])}
    return header


def get_user(token):
    # header = {"Authorization": "Bearer {0}".format(token['access_token'])}
    header = _get_header(token)
    response = requests.get('https://api.spotify.com/v1/me', headers=header)
    items = response.json()
    return items.get('id')


class Token:
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"

    def __init__(self):
        self.scope = 'streaming, user-read-email, user-read-private, user-top-read'
        self.token = None
        self.cache_path = None
        self.sp_oauth = None
        self.token_info = None
        self.code = None
        self.user = None
        self.state = None

    def get_token(self, user):
        self.user = user
        self.token = self.prompt_for_user_token(client_id=spotipy_client_id,
                                                client_secret=spotipy_client_secret,
                                                redirect_uri=spotipy_redirect_uri)
        return self.token

    def prompt_for_user_token(self, client_id=None, client_secret=None, redirect_uri=None,
                              cache_path=None):
        if self.user.spotifydata.exists():
            self.cache_path = cache_path or ".cache-" + self.user.spotifydata.sp_name
        else:
            self.cache_path = cache_path
        self.sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
                                            scope=self.scope, cache_path=self.cache_path)
        self.token_info = self.get_cached_token()
        if not self.token_info:
            auth_url = self.sp_oauth.get_authorize_url()
            data = {
                "oauth": self.sp_oauth,
                "auth_url": auth_url
            }
            return data
        else:
            return self.token_info

    def get_cached_token(self):
        token_info = None
        try:
            if self.user.spotifydata.exists():
                if is_token_expired(self.user.spotifydata.expires_in):
                    token_info = self.refresh_access_token(self.user)
        except IOError:
            pass
        return token_info

    def get_access_token(self, user=None, code=None, as_dict=True, check_cache=True):
        self.user = user
        if self.user.spotifydata.exists():
            self.cache_path = None or ".cache-" + self.user.spotifydata.sp_name
        else:
            self.cache_path = None
        self.sp_oauth = oauth2.SpotifyOAuth(spotipy_client_id, spotipy_client_secret, spotipy_redirect_uri,
                                            scope=self.scope, cache_path=self.cache_path)
        if check_cache:
            token_info = self.get_cached_token()
            if token_info is not None:
                if is_token_expired(token_info):
                    token_info = self.sp_oauth.refresh_access_token(token_info["refresh_token"])
                return token_info if as_dict else token_info["access_token"]

        payload = {
            "redirect_uri": spotipy_redirect_uri,
            "code": code,
            "grant_type": "authorization_code",
        }
        if self.scope:
            payload["scope"] = self.scope
        if self.state:
            payload["state"] = None

        headers = _make_authorization_headers(spotipy_client_id, spotipy_client_secret)

        response = requests.post(
            self.OAUTH_TOKEN_URL,
            data=payload,
            headers=headers,
            verify=True,
            timeout=None,
        )
        if response.status_code != 200:
            print('Status Code error')
        token_info = response.json()
        token_info = self._add_custom_values_to_token_info(token_info)
        user_id = get_user(token_info)
        _save_token_info(user, token_info, user_id)

    def _add_custom_values_to_token_info(self, token_info):
        token_info["expires_at"] = int(time.time()) + token_info["expires_in"]
        token_info["scope"] = self.scope
        return token_info

    def refresh_access_token(self, user):
        data = SpotifyData.objects.get(user=user)
        refresh_token = data.refresh_token
        payload = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        headers = _make_authorization_headers(spotipy_client_id, spotipy_client_secret)

        response = requests.post(
            self.OAUTH_TOKEN_URL,
            data=payload,
            headers=headers,
            proxies=None,
            timeout=None,
        )
        if response.status_code != 200:
            print('Status Code error')
        token_info = response.json()
        token_info = self._add_custom_values_to_token_info(token_info)
        if "refresh_token" not in token_info:
            token_info["refresh_token"] = refresh_token
        data.access_token = token_info['access_token']
        data.refresh_token = token_info['refresh_token']
        data.expires_at = token_info['expires_at']
        data.save()
        return token_info
