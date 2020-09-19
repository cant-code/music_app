from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from rest_framework.decorators import permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from rest_framework import status
from spotify.tokens import Token
from spotify.api_calls import Playback
from spotify.models import SpotifyData
import json
# Create your views here.


class SpotifyDataView(RetrieveUpdateAPIView, generic.View):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            data = SpotifyData.objects.get(user=self.request.user)
        except SpotifyData.DoesNotExist:
            return HttpResponse('User not found', status=404)
        serializer = serializers.SpotifySerializer(data)
        return Response(serializer.data)


class GetToken(RetrieveUpdateAPIView, generic.View):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            token = Token(self.request.user)
            data = token.prompt_for_user_token()
            if 'auth_url' in data:
                return HttpResponse(data['auth_url'], status=200)
        except:
            return HttpResponse('User already exists', status=409)


class DefineToken(RetrieveUpdateAPIView, generic.View):
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


class RefreshToken(RetrieveUpdateAPIView, generic.View):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        token = Token(self.request.user)
        token_info = token.refresh_access_token()
        # if token_info.status_code:
        #     if token_info.status_code != 200:
        #         return HttpResponse(token_info, status=token_info.status_code)
        token_info = json.dumps(token_info)
        return HttpResponse(token_info, status=200)


class MusicPlayer(LoginRequiredMixin, generic.ListView):
    template_name = 'test.html'
    model = SpotifyData

    def get_context_data(self, **kwargs):
        token = Token(user=self.request.user)
        self.data = token.refresh_access_token()
        context = super().get_context_data(**kwargs)
        context['data'] = self.data
        return context


class PlayPause(APIView, generic.View):
    permission_classes(IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        player = Playback(user=self.request.user)
        param = request.GET.get('type')
        device = request.GET.get('device_id')
        if param == 'play':
            player.start_playback(device)
        else:
            player.pause_playback()
        return HttpResponse('OK', status=200)


@permission_classes([IsAuthenticated])
def play(request):
    player = Playback(user=self.request.user)
    player.start_playback(request.user)
    return HttpResponse('OK', status=200)


@permission_classes([IsAuthenticated])
def pause(request):
    player = Playback()
    player.pause_playback(request.user)
    return HttpResponse('OK', status=200)
