from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models
UserModel = get_user_model()


class SpotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SpotifyData
        fields = ['sp_name', 'access_token', 'token_type', 'expires_in', 'refresh_token', 'expires_at']


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = 'pk'
