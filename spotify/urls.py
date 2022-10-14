from django.urls import path

from .views import SpotifyRegisterView, SpotifyCallbackView, CurrentTrackView, CurrentTrackBannerView

urlpatterns = [
    path("register/", SpotifyRegisterView.as_view()),
    path("register/callback/", SpotifyCallbackView.as_view()),
    path("<uuid:auth_id>/current-track/", CurrentTrackView.as_view()),
    path("<uuid:auth_id>/current-track/banner/", CurrentTrackBannerView.as_view()),
]
