from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class SpotifyData(models.Model):
    user = models.ForeignKey(User, related_name='spotifydata', on_delete=models.CASCADE)
    sp_name = models.CharField(max_length=256)
    access_token = models.CharField(max_length=256)
    refresh_token = models.CharField(max_length=256)
    expires_at = models.BigIntegerField()
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.sp_name
