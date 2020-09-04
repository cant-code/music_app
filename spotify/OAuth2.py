class SpotifyOAuth:
    OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"


    def _is_scope_subset(self, needle_scope, haystack_scope):
        needle_scope = set(needle_scope.split()) if needle_scope else set()
        haystack_scope = (
            set(haystack_scope.split()) if haystack_scope else set()
        )
        return needle_scope <= haystack_scope

    def is_token_expired(self, token_info):
        return is_token_expired(token_info)



    def parse_response_code(self, url):
        """ Parse the response code in the given response url
            Parameters:
                - url - the response url
        """
        _, code = self.parse_auth_response_url(url)
        if code is None:
            return url
        else:
            return code

    @staticmethod
    def parse_auth_response_url(url):
        query_s = urlparse(url).query
        form = dict(parse_qsl(query_s))
        if "error" in form:
            raise SpotifyOauthError("Received error from auth server: "
                                    "{}".format(form["error"]),
                                    error=form["error"])
        return tuple(form.get(param) for param in ["state", "code"])

    def _make_authorization_headers(self):
        return _make_authorization_headers(self.client_id, self.client_secret)

    def _open_auth_url(self):
        auth_url = self.get_authorize_url()
        try:
            webbrowser.open(auth_url)
            logger.info("Opened %s in your browser", auth_url)
        except webbrowser.Error:
            logger.error("Please navigate here: %s", auth_url)

    def _get_auth_response_interactive(self, open_browser=True):
        if open_browser:
            self._open_auth_url()
            prompt = "Enter the URL you were redirected to: "
        else:
            url = self.get_authorize_url()
            prompt = (
                "Go to the following URL: {}\n"
                "Enter the URL you were redirected to: ".format(url)
            )
        response = self._get_user_input(prompt)
        state, code = SpotifyOAuth.parse_auth_response_url(response)
        if self.state is not None and self.state != state:
            raise SpotifyStateError(self.state, state)
        return code

    def _get_auth_response_local_server(self, redirect_port):
        server = start_local_http_server(redirect_port)
        self._open_auth_url()
        server.handle_request()

        if self.state is not None and server.state != self.state:
            raise SpotifyStateError(self.state, server.state)

        if server.auth_code is not None:
            return server.auth_code
        elif server.error is not None:
            raise SpotifyOauthError("Received error from OAuth server: {}".format(server.error))
        else:
            raise SpotifyOauthError("Server listening on localhost has not been accessed")

    def get_auth_response(self, open_browser=True):
        logger.info('User authentication requires interaction with your '
                    'web browser. Once you enter your credentials and '
                    'give authorization, you will be redirected to '
                    'a url.  Paste that url you were directed to to '
                    'complete the authorization.')

        redirect_info = urlparse(self.redirect_uri)
        redirect_host, redirect_port = get_host_port(redirect_info.netloc)

        if (
            open_browser
            and redirect_host in ("127.0.0.1", "localhost")
            and redirect_info.scheme == "http"
        ):
            # Only start a local http server if a port is specified
            if redirect_port:
                return self._get_auth_response_local_server(redirect_port)
            else:
                logger.warning('Using `%s` as redirect URI without a port. '
                               'Specify a port (e.g. `%s:8080`) to allow '
                               'automatic retrieval of authentication code '
                               'instead of having to copy and paste '
                               'the URL your browser is redirected to.',
                               redirect_host, redirect_host)

        return self._get_auth_response_interactive(open_browser=open_browser)

    def get_authorization_code(self, response=None):
        if response:
            return self.parse_response_code(response)
        return self.get_auth_response()

    def get_access_token(self, code=None, as_dict=True, check_cache=True):
        """ Gets the access token for the app given the code
            Parameters:
                - code - the response code
                - as_dict - a boolean indicating if returning the access token
                            as a token_info dictionary, otherwise it will be returned
                            as a string.
        """
        if as_dict:
            warnings.warn(
                "You're using 'as_dict = True'."
                "get_access_token will return the token string directly in future "
                "versions. Please adjust your code accordingly, or use "
                "get_cached_token instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        if check_cache:
            token_info = self.get_cached_token()
            if token_info is not None:
                if is_token_expired(token_info):
                    token_info = self.refresh_access_token(
                        token_info["refresh_token"]
                    )
                return token_info if as_dict else token_info["access_token"]

        payload = {
            "redirect_uri": self.redirect_uri,
            "code": code or self.get_auth_response(),
            "grant_type": "authorization_code",
        }
        if self.scope:
            payload["scope"] = self.scope
        if self.state:
            payload["state"] = self.state

        headers = self._make_authorization_headers()

        response = self._session.post(
            self.OAUTH_TOKEN_URL,
            data=payload,
            headers=headers,
            verify=True,
            proxies=self.proxies,
            timeout=self.requests_timeout,
        )
        if response.status_code != 200:
            error_payload = response.json()
            raise SpotifyOauthError(
                'error: {0}, error_description: {1}'.format(
                    error_payload['error'], error_payload['error_description']),
                error=error_payload['error'],
                error_description=error_payload['error_description'])
        token_info = response.json()
        token_info = self._add_custom_values_to_token_info(token_info)
        self._save_token_info(token_info)
        return token_info if as_dict else token_info["access_token"]

    def _normalize_scope(self, scope):
        if scope:
            scopes = sorted(scope.split())
            return " ".join(scopes)
        else:
            return None

    def refresh_access_token(self, refresh_token):
        payload = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        headers = self._make_authorization_headers()

        response = self._session.post(
            self.OAUTH_TOKEN_URL,
            data=payload,
            headers=headers,
            proxies=self.proxies,
            timeout=self.requests_timeout,
        )

        try:
            response.raise_for_status()
        except BaseException:
            logger.error('Couldn\'t refresh token. Response Status Code: %s '
                         'Reason: %s', response.status_code, response.reason)

            message = "Couldn't refresh token: code:%d reason:%s" % (
                response.status_code,
                response.reason,
            )
            raise SpotifyException(response.status_code,
                                   -1,
                                   message,
                                   headers)

        token_info = response.json()
        token_info = self._add_custom_values_to_token_info(token_info)
        if "refresh_token" not in token_info:
            token_info["refresh_token"] = refresh_token
        self._save_token_info(token_info)
        return token_info

    def _add_custom_values_to_token_info(self, token_info):
        """
        Store some values that aren't directly provided by a Web API
        response.
        """
        token_info["expires_at"] = int(time.time()) + token_info["expires_in"]
        token_info["scope"] = self.scope
        return token_info