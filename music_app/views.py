from django.http import JsonResponse
from django.views.generic import TemplateView
import django.middleware.csrf


class HomeView(TemplateView):
    template_name = 'index.html'


def get_csrf_token(request):
    token = django.middleware.csrf.get_token(request)
    return JsonResponse({'token': token})
