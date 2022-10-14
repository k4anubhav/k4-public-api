from PIL import Image
from django.http import HttpResponse
from django.shortcuts import redirect, resolve_url
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from .client import SpotifyClient
from .exceptions import NoTrackPlaying
from .mixins import SpotifyClientMixin
from .models import SpotifyToken
from .serializers import CurrentTrackSerializer
from .utils import SpotifyBanner


class SpotifyRegisterView(GenericAPIView):

    @staticmethod
    def get(request):
        url = SpotifyClient.get_oauth_url()
        return redirect(url)


class SpotifyCallbackView(GenericAPIView):

    @staticmethod
    def get(request: Request):
        url = request.get_full_path()
        client = SpotifyClient()
        code = client.auth_manager.get_authorization_code(url)
        client.auth_manager.get_access_token(code)
        token: SpotifyToken = client.get_spotify_token()
        return redirect(resolve_url('current-track-banner', auth_id=token.id))


class CurrentTrackView(SpotifyClientMixin, RetrieveAPIView):
    serializer_class = CurrentTrackSerializer

    def get_object(self):
        current_track = self.client.current_user_playing_track()
        if not current_track:
            raise NoTrackPlaying
        return current_track


class CurrentTrackBannerView(SpotifyClientMixin, GenericAPIView):

    def get(self, request, *args, **kwargs):
        track = self.client.current_user_playing_track()
        if track:
            banner = SpotifyBanner(track).banner
        else:
            banner = Image.open('doc/spotify/NotListening.png')

        response = HttpResponse(content_type='image/png')
        # noinspection PyTypeChecker
        banner.save(response, 'PNG')
        return response


class CurrentTrackRedirectView(SpotifyClientMixin, GenericAPIView):
    def get(self, request):
        current_track = self.client.current_user_playing_track()
        if current_track:
            return redirect(current_track.external_urls['spotify'])
        return Response(status=status.HTTP_204_NO_CONTENT)
