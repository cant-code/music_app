from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
import django.middleware.csrf
from rest_framework.decorators import api_view


class HomeView(TemplateView):
    template_name = 'index.html'


@api_view(['GET'])
def get_csrf_token(request):
    token = django.middleware.csrf.get_token(request)
    return JsonResponse({'token': token})
