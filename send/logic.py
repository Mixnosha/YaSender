import yagmail
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from psycopg2.sql import NULL

from send.models import RecipientEmail, SendEmail, GroupEmail


def add_rec_email(request):
    email = request.POST.get('email')
    user = User.objects.get(username=request.POST.get('user'))
    RecipientEmail.objects.create(email=email, user=user)
    return redirect(reverse('recipient:recipient_all_view', kwargs={'username': request.user.username}))


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
    except Exception:
        return HttpResponse(f'Please check that the username and password are correct: \n {email}')
    return redirect('/')

def del_email(request):
    id = request.GET.get('del_email_id')
    if request.GET.get('type_email') == 'send_email':
        del_e = SendEmail.objects.get(id=id)
        del_e.delete()
    elif request.GET.get('type_email') == 'to_emails':
        print('to_emails')
        del_e = RecipientEmail.objects.get(id=id)
        del_e.delete()
    elif request.GET.get('type_email') == 'group':
        del_e = GroupEmail.objects.get(id=id)
        emails = RecipientEmail.objects.filter(group=del_e)
        for email in emails:
            email.group = None
            email.save()
        del_e.delete()
    return redirect(reverse('recipient:recipient_all_view', kwargs={'username': request.user.username}))


def create_group_def(request):
    emails_to_group_id = request.POST.getlist('emails')
    if len(emails_to_group_id) < 2:
        return HttpResponse('Select min 2 mail')
    name_group = request.POST.get('name_group')
    group = GroupEmail.objects.create(user=request.user, name_group=name_group)
    for id in emails_to_group_id:
        rec_email = RecipientEmail.objects.get(id=id)
        rec_email.group = group
        rec_email.save()
    return redirect('account')



