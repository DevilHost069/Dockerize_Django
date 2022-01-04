from django.contrib import admin
from .models import Userprofile,MailMessage,Subscribers
# Register your models here.

admin.site.register(Userprofile)
admin.site.register(MailMessage)
admin.site.register(Subscribers)