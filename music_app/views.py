from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
import django.middleware.csrf


class HomeView(TemplateView):
    template_name = 'index.html'


def get_csrf_token(request):
    if request.method == 'GET':
        token = django.middleware.csrf.get_token(request)
        return JsonResponse({'token': token})
    return HttpResponse(status=405)
