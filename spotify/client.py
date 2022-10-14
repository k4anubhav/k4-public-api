import logging
from typing import Optional

from spotipy import SpotifyOAuth, Spotify, CacheHandler

from spotify.models import SpotifyToken

logger = logging.getLogger(__name__)


class SpotifyCacheHandler(CacheHandler):

    def __init__(self, token: Optional[SpotifyToken] = None):
        self.token = token

    def get_cached_token(self):
        """
        Get and return a token_info dictionary object.
        """
        if self.token:
            return self.token.token_info()
        return None

    def save_token_to_cache(self, token_info):
        """
        Save a token_info dictionary object to the cache and return None.
        """
        if self.token:
            for key, value in token_info.items():
                setattr(self.token, key, value)
            self.token.save()
        else:
            self.token = SpotifyToken.objects.create(**token_info)
        return None


class SpotifyClient(Spotify):
    def __init__(self, token: Optional[SpotifyToken] = None):
        super().__init__(
            auth_manager=SpotifyOAuth(
                scope="user-read-currently-playing",
                open_browser=False,
                cache_handler=SpotifyCacheHandler(token),
            )
        )

    @staticmethod
    def get_oauth_url():
        return SpotifyOAuth(
            scope="user-read-currently-playing",
            open_browser=False,
        ).get_authorize_url()

    def get_spotify_token(self):
        cache_handler: SpotifyCacheHandler = self.auth_manager.cache_handler
        return cache_handler.token
