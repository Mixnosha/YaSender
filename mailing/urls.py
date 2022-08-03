from django.contrib import admin
from django.urls import path

from send.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', RegisterUser.as_view(), name='register'),
    path('login', LoginUser.as_view(), name='login'),
]
