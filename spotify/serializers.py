from rest_framework import serializers


class ArtistSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    href = serializers.URLField(source='external_urls.spotify')


class Track(serializers.Serializer):
    artists = ArtistSerializer(many=True)
    duration_ms = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    href = serializers.URLField(source='external_urls.spotify')
    preview_url = serializers.URLField()
    explicit = serializers.BooleanField()


class CurrentTrackSerializer(serializers.Serializer):
    track = Track(source='item')
    progress_ms = serializers.IntegerField()
    is_playing = serializers.BooleanField()
