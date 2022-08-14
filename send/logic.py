from smtplib import SMTPAuthenticationError

import yagmail
import time
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from psycopg2.sql import NULL

from recipient.logic import check_for_uniqueness_mails, redirect_with_params
from send.models import RecipientEmail, SendEmail, GroupEmail




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

def send_all_email(request):
    email = SendEmail.objects.get(id=request.POST.get('send_email'))
    password = email.password
    email = email.email
    subject = request.POST.get('subject')
    body = request.POST.get('text')
    to = RecipientEmail.objects.filter(user=request.user)
    try:
        yag = yagmail.SMTP(user=email, password=password, host='smtp.gmail.com')
        yag.send(to=to, subject=subject, contents=[body, ])
    except Exception:
        return HttpResponse(f'Please check that the username and password are correct: \n {email}')
    return redirect('/')

def send_email(request):
    if request.POST.get('all_emails'):
        send_all_email(request)
    email = SendEmail.objects.get(id=request.POST.get('send_email'))
    password = email.password
    email = email.email
    subject = request.POST.get('subject')
    body = request.POST.get('text')
    if not request.POST.get('groups'):
        to = request.POST.getlist('emails')
        try:
            yag = yagmail.SMTP(user=email, password=password, host='smtp.gmail.com')
            yag.send(to=to, subject=subject, contents=[body, ])
        except Exception as e:
            print(e)
        return HttpResponse(f'Please check that the username and password are correct: \n {email}')
    else:
        id_group = request.POST.get('groups')
        group = GroupEmail.objects.get(id=id_group)
        to = [i.email for i in RecipientEmail.objects.filter(groups=group)]
        try:
            start_time = time.time()
            yag = yagmail.SMTP(user=email, password=password, host='smtp.gmail.com')
            print('Отправка пошла')
            yag.send(to=to, subject=subject, contents=[body, ])

            print("--- %s seconds ---" % (time.time() - start_time))
            print("Отправка завершилась")
        except Exception as e:
            print(e)
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
        del_e.delete()
    return redirect(reverse('recipient:recipient_all_view', kwargs={'username': request.user.username}))


def create_group_def(request):
    emails_to_group_id = request.POST.getlist('emails')
    name_group = request.POST.get('name_group')
    try:
        GroupEmail.objects.get(name_group=name_group, user=request.user)
        return redirect_with_params('account', error_unique=True)
    except Exception:
        group = GroupEmail.objects.create(user=request.user, name_group=name_group)
    if request.POST.get('select_all_emails'):
        for r in RecipientEmail.objects.filter(user=request.user):
            r.groups.add(group)
        return redirect_with_params('account', error_unique=False)
    if len(emails_to_group_id) < 2:
        return HttpResponse('Select min 2 mail')
    for id in emails_to_group_id:
        rec_email = RecipientEmail.objects.get(id=id)
        rec_email.groups.add(group)
        rec_email.save()
    return redirect_with_params('account', error_unique=False)
