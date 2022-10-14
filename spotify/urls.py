from django.urls import path

from .views import SpotifyRegisterView, SpotifyCallbackView, CurrentTrackView, CurrentTrackBannerView

urlpatterns = [
    path("register/", SpotifyRegisterView.as_view(), name="register"),
    path("register/callback/", SpotifyCallbackView.as_view(), name="spotify-callback"),
    path("<uuid:auth_id>/current-track/", CurrentTrackView.as_view(), name="current-track"),
    path("<uuid:auth_id>/current-track/banner/", CurrentTrackBannerView.as_view(), name="current-track-banner"),
]
