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
    try:
        yag = yagmail.SMTP(user=email, password=password, host='smtp.gmail.com')
        yag.send(subject='YaSender', contents='Successfully!\nYour mail has been successfully added')
        SendEmail.objects.create(email=email, user=user, password=password)
        return redirect('account')
    except Exception:
        return HttpResponse('Check if the data is correct!')


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
        SendEmail.objects.create()
    except Exception:
        return HttpResponse(f'Please check that the username and password are correct: \n {email}')
    return redirect('/')

def del_email(request):
    id = request.GET.get('del_email_id')
    if request.GET.get('type_email') == 'send_email':
        del_e = SendEmail.objects.get(id=id)
        del_e.delete()
    else:
        del_e = RecipientEmail.objects.get(id=id)
        del_e.delete()
    return redirect('account')