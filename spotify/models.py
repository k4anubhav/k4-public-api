import uuid

from django.db import models


class SpotifyToken(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=255)
    expires_in = models.IntegerField()
    expires_at = models.IntegerField()
    scope = models.TextField()
    refresh_token = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.created_at} - {self.token_type}"

    def token_info(self):
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "expires_at": self.expires_at,
            "scope": self.scope,
            "refresh_token": self.refresh_token,
        }
