import urllib

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from validate_email import validate_email
from send.models import RecipientEmail, GroupEmail


def redirect_with_params(viewname, url_param=None, **kwargs):
    if url_param != None:
        key = list(url_param.keys())[0]
        val = url_param[key]
        rev = reverse(viewname, kwargs={key: val})
    else:
        rev = reverse(viewname)
    params = urllib.parse.urlencode(kwargs)
    if params:
        rev = '{}?{}'.format(rev, params)

    return HttpResponseRedirect(rev)
def check_for_uniqueness_mails(request, mails):
    added = 0
    errors = 0
    unique_mail = []
    for mail in mails:
        try:
            RecipientEmail.objects.get(email=mail, user=request.user)
            errors += 1
        except Exception:
            if validate_email(email=mail):
                added += 1
                unique_mail.append(mail)
            else:
                errors += 1
    return {'added': added,
            'errors': errors,
            'unique_mail': unique_mail}


def add_email_for_file(request):
    if request.method == "POST":
        file = request.FILES["file"]
        mails = []
        try:
            for line in file.readlines():
                mails.append(line.decode('UTF-8'))
        except UnicodeDecodeError:
            return redirect_with_params(
                'recipient:recipient_all_view',
                url_param={'username': request.user.username},
                file_error=True,
            )

        res = check_for_uniqueness_mails(request, mails)
        groups = get_groups_html(request)
        for mail in res['unique_mail']:
            obj = RecipientEmail.objects.create(user=request.user, email=mail)
            for group in groups:
                try:
                    g = GroupEmail.objects.get(name_group=group, user=request.user)
                    obj.groups.add(g)
                except Exception:
                    g = g = GroupEmail.objects.create(name_group=group, user=request.user)
                    obj.groups.add(g)
            obj.save()
    return redirect_with_params(
        'recipient:recipient_all_view',
        url_param={'username': request.user.username},
        added=res['added'],
        errors=res['errors']
    )

def add_rec_email(request):
    mail = request.POST.get('email')
    res = check_for_uniqueness_mails(request, [mail, ])
    user = User.objects.get(username=request.POST.get('user'))
    try:
        RecipientEmail.objects.create(email=res['unique_mail'][0], user=user)
    except Exception:
        pass
    return redirect_with_params(
        'recipient:recipient_all_view',
        url_param={'username': request.user.username},
        added=res['added'],
        errors=res['errors']
    )

def get_groups_html(request):
    groups = []
    for num in range(1,6):
        if request.POST.get('name_group'+str(num)):
            groups.append(request.POST.get('name_group'+str(num)))
        else:
            break
    return groups
