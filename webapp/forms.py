from django import forms
from webapp.models import User, Category, Event


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
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
