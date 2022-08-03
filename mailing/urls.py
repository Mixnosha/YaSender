from django.contrib import admin
from django.urls import path

from send.logic import add_rec_email, add_send_email
from send.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', SendEmailView.as_view(), name='main_page'),
    path('register', RegisterUser.as_view(), name='register'),
    path('login', LoginUser.as_view(), name='login'),
    path('account', AccountView.as_view(), name='account'),
    path('add_rec_email', add_rec_email, name='add_rec_email'),
    path('add_send_email', add_send_email, name='add_send_email')


]
