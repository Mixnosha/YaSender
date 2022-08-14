from django.urls import path

from groups.views import GroupMainPage

app_name = 'groups'
urlpatterns = [
    path('', GroupMainPage.as_view(), name='index_group' )
]