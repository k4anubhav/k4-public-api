from rest_framework.exceptions import APIException


class NoTrackPlaying(APIException):
    status_code = 204
    default_detail = 'No track is playing.'
    default_code = 'no_track_playing'
