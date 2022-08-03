from django.conf import settings
from django.db import models


class Email(models.Model):
    Type = [
        ("sender", "sender"), ("recipient", "recipient")
    ]
    type = models.CharField(choices=Type, max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.email


class GroupEmail(models.Model):
    name_group = models.CharField(max_length=255)
    email = models.ForeignKey('Email', on_delete=models.CASCADE)

    def __str__(self):
        return self.name_group

class CustomizeUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    groups = models.ForeignKey('GroupEmail', on_delete=models.CASCADE)
    email = models.ForeignKey('Email', on_delete=models.CASCADE)

    def __str__(self):
        return self.user
