from django.urls import path

from groups.views import GroupMainPage, ViewOneGroup

app_name = 'groups'
urlpatterns = [
    path('', GroupMainPage.as_view(), name='index_group'),
    path('<str:name_group>/', ViewOneGroup.as_view(), name='one_group')

]