from django.shortcuts import render
from django.views.generic import ListView

from send.models import GroupEmail


class GroupMainPage(ListView):
    template_name = 'groups/group_index.html'
    queryset = GroupEmail.objects.all()
    context_object_name = 'groups'
