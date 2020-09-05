from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
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


class SpotifyDataView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            data = SpotifyData.objects.get(pk=self.request.user.pk)
        except SpotifyData.DoesNotExist:
            raise Http404
        serializer = serializers.SpotifySerializer(data)
        return Response(serializer.data)


class GetToken(RetrieveUpdateAPIView, generic.View):
    serializer_class = serializers.UserDetailsSerializer
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


def play(request):
    token = Token()
    player = Playback()
    data = token.refresh_access_token(request.user)
    player.start_playback(data)
    return HttpResponse('OK', status=200)


def pause(request):
    token = Token()
    player = Playback()
    data = token.refresh_access_token(request.user)
    player.pause_playback(data)
    return HttpResponse('OK', status=200)
