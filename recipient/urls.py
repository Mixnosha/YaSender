from django.urls import path

from recipient.logic import add_email_for_file
from recipient.views import RecipientAllView


app_name = 'recipient'
urlpatterns = [
    path('add_email_for_file', add_email_for_file, name='add_email_for_file'),
    path('<str:username>', RecipientAllView.as_view(), name="recipient_all_view"),



]