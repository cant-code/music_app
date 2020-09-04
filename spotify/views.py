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
from spotify.tokens import authenticate, Token
from spotify.api_calls import Playback
from spotify.models import SpotifyData
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
            token = Token()
            data = token.get_token(self.request.user)
            if 'auth_url' in data:
                return HttpResponse(data['auth_url'], status=200)
        except:
            return HttpResponse('User already exists', status=409)


class DefineToken(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('accounts:acc_mgr')

    def get(self, request, *args, **kwargs):
        url = request.get_full_path()
        authenticate(self.request.user, url)
        return redirect('accounts:acc_mgr')


class MusicPlayer(LoginRequiredMixin, generic.ListView):
    template_name = 'test.html'
    model = SpotifyData

    def get_context_data(self, **kwargs):
        token = Token()
        self.data = token.refresh_access_token(self.request.user)
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
