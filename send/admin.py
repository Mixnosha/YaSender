from django.contrib import admin

from send.models import *

admin.site.register(SendEmail)
admin.site.register(RecipientEmail)
admin.site.register(GroupEmail)
