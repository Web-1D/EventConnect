from django import forms
<<<<<<< HEAD
from webapp.models import User, Category, Event, Comment, QAForum
from django.contrib.auth.models import User
=======
from webapp.models import User, Category, Event

>>>>>>> 30df37d694ec9f0601bd503bd8c346f8af5f9b03

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
<<<<<<< HEAD

    class Meta:
        model = User
        fields = ('username', 'password',)
=======
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
>>>>>>> 30df37d694ec9f0601bd503bd8c346f8af5f9b03
