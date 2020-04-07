from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from . import forms
# Create your views here.
User = get_user_model()


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class AccountManager(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/accounts_base.html'
