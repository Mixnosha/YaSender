from django.contrib.auth import logout,  login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView
from send.forms import RegisterUserForms, LoginUserForm, AddRecipientEmailForm, AddSendEmailForm, SendEmailForm
from send.models import SendEmail, RecipientEmail, GroupEmail


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
        login(self.request, user)
        return redirect('account')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'register/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

    def get_success_url(self):
        return reverse_lazy('account')


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
                'form_add_rec_email': AddRecipientEmailForm(),
                'form_add_send_email': AddSendEmailForm(),
                'rec_emails': RecipientEmail.objects.filter(user=self.request.user),
                'groups': GroupEmail.objects.filter(user=self.request.user)
            }
        )
        return context


class SendEmailView(FormView):
    template_name = 'send/sendemail.html'
    form_class = SendEmailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'rec_emails': RecipientEmail.objects.filter(user=self.request.user)
            }
        )
        return context


def logout_user(request):
    logout(request)
    return redirect('register')

