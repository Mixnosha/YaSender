from django.contrib import admin
from django.urls import path, include
from send.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('send.urls')),
    path('recipient/', include('recipient.urls')),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login', LoginUser.as_view(), name='login'),
    path('account', AccountView.as_view(), name='account'),

]
