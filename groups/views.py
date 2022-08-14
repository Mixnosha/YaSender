from django.shortcuts import render
from django.views.generic import ListView

from send.models import GroupEmail


class GroupMainPage(ListView):
    template_name = 'groups/group_index.html'
    queryset = GroupEmail.objects.all()
    context_object_name = 'groups'

class ViewOneGroup(ListView):
    template_name = 'groups/onegroup.html'
    context_object_name = 'group'

    def get_queryset(self):
        return GroupEmail.objects.get(name_group=self.kwargs['name_group'])