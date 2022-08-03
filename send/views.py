from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
import smtplib

from django.views.generic import CreateView

from send.forms import RegisterUserForms, LoginUserForm


class RegisterUser(CreateView):
    form_class = RegisterUserForms
    template_name = 'register/register.html'
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

    def form_valid(self, form):
        user = form.save()
        return redirect('/')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'register/login.html'
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context
