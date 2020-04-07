import spotipy
import spotipy.oauth2 as oauth2
import os

spotipy_client_id = os.environ.get('spotipy_client_id')
spotipy_client_secret = os.environ.get('spotipy_client_secret')
spotipy_redirect_uri = os.environ.get('spotipy_redirect_uri')


def get_token(user):
    username = user
    scope = 'user-top-read'
    token = prompt_for_user_token(username, scope, client_id=spotipy_client_id,
                                  client_secret=spotipy_client_secret,
                                  redirect_uri=spotipy_redirect_uri)
    return token


def get_data(token, username, term, size, search_type):
    if token:
        token2 = token['token']
        sp = spotipy.Spotify(auth=token2)
        sp.trace = False
        # print(sp.recommendations(seed_artists=['1vCWHaC5f2uS3yhpwWbIA6'], seed_tracks=['322tcqPhma7F6hfCeLisx0']))
        # print(sp._get('search', q='Radiohead', limit=20, offset=0, type='track,album', market=None))
        result = []
        results = None
        try:
            results2 = sp.user(username)
            result.append(results2)
        except spotipy.SpotifyException:
            return 404
        if size is None:
            size = 5
        if search_type is "Track":
            results = sp.current_user_top_tracks(time_range=term, limit=size)
        if search_type is "Artist":
            results = sp.current_user_top_artists(time_range=term, limit=size)
        result.append(results)
        return result
    else:
        return None


def prompt_for_user_token(username, scope=None, client_id=None,
                          client_secret=None, redirect_uri=None,
                          cache_path=None):
    cache_path = cache_path or ".cache-" + username
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
                                   scope=scope, cache_path=cache_path)
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        data = {
            "oauth": sp_oauth,
            "auth_url": auth_url
        }
        return data
    else:
        return token_info


def authenticate(sp_oauth, response):
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)
    if token_info:
        return {"token": token_info['access_token']}
    else:
        return None


def search(token, username, query, limit, types):
    token2 = token['token']
    sp = spotipy.Spotify(auth=token2)
    sp.trace = False
    result = []
    try:
        results2 = sp.user(username)
        result.append(results2)
    except spotipy.SpotifyException:
        return 404
    string = types[0]
    string = ','.join(types)
    result.append(sp._get('search', q=query, limit=limit, offset=0, type=string, market=None))
    return result


def recommendations(token, username, data, limit):
    token2 = token['token']
    sp = spotipy.Spotify(auth=token2)
    sp.trace = False
    result = []
    artists = []
    tracks = []
    for i in data:
        if i.get('type') == 'tracks':
            tracks.append(i.get('d_id'))
        else:
            artists.append(i.get('d_id'))
    try:
        results2 = sp.user(username)
        result.append(results2)
    except spotipy.SpotifyException:
        return 404
    result.append(sp.recommendations(seed_artists=artists, seed_tracks=tracks, limit=limit))
    return result
