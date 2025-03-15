from django import forms
from webapp.models import User, Category, Event, Comment, QAForum
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    #

class EventForm(forms.ModelForm):
    #

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password',)
