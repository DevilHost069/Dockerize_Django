from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from .models import Userprofile

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Userprofile.objects.create(
            user = user,
            email = user.email,
            name = user.first_name
        )
        
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.email = profile.email
        user.save()
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()
post_save.connect(createProfile,sender=User)
post_save.connect(updateUser,sender=Userprofile)
post_delete.connect(deleteUser, sender=Userprofile)