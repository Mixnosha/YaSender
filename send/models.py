from django.conf import settings
from django.db import models


class GroupEmail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name_group = models.CharField(max_length=255)

    def __str__(self):
        return self.name_group


class SendEmail(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    password = models.CharField(max_length=50)
    group = models.ForeignKey('GroupEmail', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.email


class RecipientEmail(models.Model):
    email = models.EmailField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey('GroupEmail', on_delete=models.CASCADE, blank=True, null=True)
    send = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class SendEmailModel(models.Model):
    send_email = models.ForeignKey('SendEmail', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.subject