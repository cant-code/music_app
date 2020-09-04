from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'spotify'

urlpatterns = [
    path('gettoken/', views.GetToken.as_view(), name='get_token'),
    path('auth/', views.DefineToken.as_view(), name='auth'),
    path('player/', views.MusicPlayer.as_view(), name='player'),
    path('player/play/', views.play),
    path('player/pause/', views.pause)
]
