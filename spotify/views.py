from django.http import HttpResponse
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import serializers
from spotify.tokens import Token
from spotify.models import SpotifyData
import json
# Create your views here.


class SpotifyDataView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            data = SpotifyData.objects.get(user=self.request.user)
        except SpotifyData.DoesNotExist:
            return HttpResponse('User not found', status=404)
        serializer = serializers.SpotifySerializer(data)
        return Response(serializer.data)


class GetToken(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            token = Token(self.request.user)
            data = token.prompt_for_user_token()
            if 'auth_url' in data:
                return HttpResponse(data['auth_url'], status=200)
        except:
            return HttpResponse('User already exists', status=409)


class DefineToken(RetrieveUpdateAPIView):
    serializer_class = serializers.SpotifySerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        token = Token(self.request.user)
        token_info = token.get_access_token(code=request.query_params.get('code'))
        # if token_info.status_code:
        #     if token_info.status_code != 200:
        #         return HttpResponse(token_info, status=token_info.status_code)
        token_info = json.dumps(token_info)
        return HttpResponse(token_info, status=200)


class RefreshToken(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        token = Token(self.request.user)
        token_info = token.refresh_access_token()
        # if token_info.status_code:
        #     if token_info.status_code != 200:
        #         return HttpResponse(token_info, status=token_info.status_code)
        token_info = json.dumps(token_info)
        return HttpResponse(token_info, status=200)
