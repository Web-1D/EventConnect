from django import forms
from webapp.models import User, Category, Event


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


from django import forms
from webapp.models import Event

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'google_maps_link']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'date': 'Date and Time (YYYY-MM-DD HH:MM)',
            'location': 'Location',
            'google_maps_link': 'Google Maps Link',
        }
        help_texts = {
            'title': 'Enter the event title',
            'description': 'Provide a brief description of the event',
            'date': 'Format: 2025-03-22 18:30',
            'location': 'Enter a name or address (for users)',
            'google_maps_link': 'Paste the full Google Maps **shareable** link (e.g. https://www.google.com/maps/place/...)',
        }



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')