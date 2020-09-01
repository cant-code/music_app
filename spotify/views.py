from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from spotify.tokens import authenticate, Token
from spotify.api_calls import Playback
from spotify.models import SpotifyData
# Create your views here.


class GetToken(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('home')

    def get(self, request, *args, **kwargs):
        try:
            token = Token()
            data = token.get_token(self.request.user)
            if 'auth_url' in data:
                return redirect(data['auth_url'])
        except:
            messages.warning(self.request, 'User already exists')
        return super().get(request, *args, **kwargs)


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
