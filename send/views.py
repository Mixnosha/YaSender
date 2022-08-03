from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
import smtplib

from django.views.generic import CreateView, ListView

from send.forms import RegisterUserForms, LoginUserForm, AddRecipientEmail, AddSendEmail
from send.models import SendEmail, RecipientEmail


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


class AccountView(ListView):
    template_name = 'send/account.html'
    context_object_name = 'send_emails'

    def get_queryset(self):
        return SendEmail.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'to_emails': RecipientEmail.objects.filter(user=self.request.user),
                'form_add_rec_email': AddRecipientEmail(),
                'form_add_send_email': AddSendEmail(),
             }
        )
        print(context['form_add_send_email'])
        return context

