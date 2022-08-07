from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from send.models import RecipientEmail


def add_email_for_file(request):
    if request.method == "POST":
        file = request.FILES["file"]
        for line in file.readlines():
            RecipientEmail.objects.create(email=line.decode('UTF-8'), user=request.user)
    return redirect(reverse('recipient:recipient_all_view', kwargs={'username': request.user.username}))
