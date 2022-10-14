from PIL import Image
from django.http import HttpResponse
from django.shortcuts import redirect
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
        return Response(
            {
                'auth_id': token.id,
            },
            status=status.HTTP_201_CREATED
        )


class CurrentTrackView(SpotifyClientMixin, RetrieveAPIView):
    serializer_class = CurrentTrackSerializer

    def get_object(self):
        track = self.client.current_user_playing_track()
        if not track:
            raise NoTrackPlaying
        return track


class CurrentTrackBannerView(SpotifyClientMixin, GenericAPIView):

    def get(self, request, *args, **kwargs):
        track = self.client.current_user_playing_track()
        if track:
            banner = SpotifyBanner(track).banner
        else:
            banner = Image.open('NotListning.png')

        response = HttpResponse(content_type='image/png')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        # noinspection PyTypeChecker
        banner.save(response, 'PNG')
        return response
