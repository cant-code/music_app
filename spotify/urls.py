from django.urls import path
from . import views

app_name = 'spotify'

urlpatterns = [
    path('gettoken/', views.GetToken.as_view(), name='get_token'),
    path('auth/', views.DefineToken.as_view(), name='auth'),
    path('get_data/', views.SpotifyDataView.as_view(), name='get_data'),
    path('refresh_token/', views.RefreshToken.as_view(), name='refresh_token'),
    path('player/', views.PlayPause.as_view(), name='player'),
    path('player/play/', views.play),
    path('player/pause/', views.pause)
]
