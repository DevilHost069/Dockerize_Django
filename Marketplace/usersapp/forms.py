from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Userprofile,Subscribers,MailMessage
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields= ['first_name', 'email', 'username', 'password1', 'password2']

class ProfileForm(ModelForm):
    class Meta:
        model = Userprofile
        exclude = ['user']
        
class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ['subs_email']

class MailMsgFrom(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = '__all__'
    