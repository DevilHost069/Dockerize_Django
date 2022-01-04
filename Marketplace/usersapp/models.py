from django.db import models
from django.db.models.fields import DateTimeField
from django.contrib.auth.models import User
import uuid

districts_choice = (
    ('SlD', 'Select District'),
    ('Mrng','Morang'),
    ('Suns', 'Sunsari'),
    ('Ilm', 'Illam'),
    ('ktm', 'Kathmandu'),
    ('chtwn', 'Chitwan'),
    ('sirh', 'Siraha')
)
class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    locations = models.CharField(max_length=200, choices=districts_choice,null=True)
    listingcity = models.CharField(max_length=200)
    phonnumber = models.BigIntegerField(null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    social_facebook = models.CharField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to ='profiles/', default='profiles/mehdi.png')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
    
class Subscribers(models.Model):
    subs_email = models.EmailField(max_length=200,blank=True,null=True)
    subs_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subs_email

class MailMessage(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(max_length=1000, blank=True,null=True)
    
    def __str__(self):
        return self.title
