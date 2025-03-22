from django import forms
from webapp.models import User, Category, Event


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class EventForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'category']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
