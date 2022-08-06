from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from send.models import RecipientEmail


class RecipientAllView(ListView):
    template_name = 'recipient/recipient_all_view.html'
    context_object_name = 'recipient_all'

    def get_queryset(self):
        return RecipientEmail.objects.filter(user__username=self.kwargs['username'])

