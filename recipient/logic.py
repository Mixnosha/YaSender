from django.shortcuts import redirect
from validate_email import validate_email
from send.models import RecipientEmail


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
        for line in file.readlines():
            mails.append(line.decode('UTF-8'))
        res = check_for_uniqueness_mails(request, mails)
        for mail in res['unique_mail']:
            RecipientEmail.objects.create(user=request.user, email=mail)
    response = redirect('recipient:recipient_all_view', username=request.user.username)
    response['Location'] += '?added=' + str(res['added'])+'&errors=' + str(res['errors'])
    return response
