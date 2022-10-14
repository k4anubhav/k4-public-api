from typing import Optional

from django.http import Http404

from spotify.client import SpotifyClient
from spotify.models import SpotifyToken


class SpotifyClientMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client: Optional[SpotifyClient] = None

    def _get_token(self) -> SpotifyToken:
        try:
            # noinspection PyUnresolvedReferences
            return SpotifyToken.objects.get(id=self.kwargs['auth_id'])
        except SpotifyToken.DoesNotExist:
            raise Http404

    @property
    def client(self) -> SpotifyClient:
        if self._client is None:
            token = self._get_token()
            self._client = SpotifyClient(token)
        return self._client
