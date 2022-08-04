import yagmail
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from send.models import RecipientEmail, SendEmail


def add_rec_email(request):
    email = request.POST.get('email')
    user = User.objects.get(username=request.POST.get('user'))
    RecipientEmail.objects.create(email=email, user=user)
    return redirect('account')


def add_send_email(request):
    email = request.POST.get('email')
    user = User.objects.get(username=request.POST.get('user'))
    password = request.POST.get('password')
    SendEmail.objects.create(email=email, user=user, password=password)
    return redirect('account')


def send_email(request):
    to = request.POST.getlist('emails')
    email = SendEmail.objects.get(id=request.POST.get('send_email'))
    password = email.password
    email = email.email
    subject = request.POST.get('subject')
    body = request.POST.get('text')
    try:
        yag = yagmail.SMTP(user=email, password=password, host='smtp.gmail.com')
        yag.send(to=to, subject=subject, contents=[body, ])
    except Exception:
        return HttpResponse(f'Please check that the username and password are correct: \n {email}')
    return redirect('/')
