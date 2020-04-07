from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class SpotifyData(models.Model):
    user = models.ForeignKey(User, related_name='spotifydata', on_delete=models.CASCADE)
    sp_name = models.TextField(max_length=256)
    access_token = models.CharField(max_length=256)
    token_type = models.CharField(max_length=256)
    expires_in = models.PositiveIntegerField()
    refresh_token = models.CharField(max_length=256)
    expires_at = models.BigIntegerField()

    def __str__(self):
        return self.sp_name

    def get_absolute_url(self):
        return reverse('spotify:single')
