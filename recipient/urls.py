from django.urls import path

from recipient.views import RecipientAllView

urlpatterns = [
    path('/<str:username>', RecipientAllView.as_view(), name="recipient_all_view"),


]