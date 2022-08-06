from django.urls import path
from send.logic import add_rec_email, add_send_email, send_email, del_email, create_group_def
from send.views import *


urlpatterns = [
    path('', SendEmailView.as_view(), name='main_page'),
    path('add_rec_email', add_rec_email, name='add_rec_email'),
    path('add_send_email', add_send_email, name='add_send_email'),
    path('send_email', send_email, name='send_email'),
    path('logout', logout_user, name='logout'),
    path('del_email', del_email, name='del_email'),
    path('create_group_def', create_group_def, name='create_group_def'),
]