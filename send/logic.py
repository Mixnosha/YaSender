# import smtplib
#
# # данные почтового сервиса
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.conf import settings
from send.models import RecipientEmail, SendEmail


#
# user = "your-address@yandex.ru"
# passwd = "**********"
# server = "smtp.gmail.com"
# port = 465
#
# # тема письма
# subject = "Тестовое письмо от Python."
# # кому
# to = "person@mail.ru"
# # кодировка письма
# charset = 'Content-Type: text/plain; charset=utf-8'
# mime = 'MIME-Version: 1.0'
# # текст письма
# text = "Отправкой почты управляет Python!"
#
# # формируем тело письма
# body = "\r\n".join((f"From: {user}", f"To: {to}",
#        f"Subject: {subject}", mime, charset, "", text))
#
# try:
#     # подключаемся к почтовому сервису
#     smtp = smtplib.SMTP(server, port)
#     smtp.starttls()
#     smtp.ehlo()
#     # логинимся на почтовом сервере
#     smtp.login(user, passwd)
#     # пробуем послать письмо
#     smtp.sendmail(user, to, body.encode('utf-8'))
# except smtplib.SMTPException as err:
#     print('Что - то пошло не так...')
#     raise err
# finally:
#     smtp.quit()


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
