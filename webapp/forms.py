from django import forms
from webapp.models import User, Category, Event, QAForum, Review


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class EventForm(forms.ModelForm):
    notify_users = forms.BooleanField(required=False, initial=False, label='Notify all users')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'google_maps_link', 'notify_users']
        labels = {
            'title': 'Title',
            'description': 'Description',
            'date': 'Date and Time (YYYY-MM-DD HH:MM)',
            'location': 'Location',
            'google_maps_link': 'EMBED Google Maps Link',
        }
        help_texts = {
            'title': 'Enter the event title',
            'description': 'Provide a brief description of the event',
            'date': 'Format: 2025-03-22 18:30',
            'location': 'Enter the address of the location',
            'google_maps_link': 'Paste the EMBED Google Maps',
        }

    def clean_google_maps_link(self):
        link = self.cleaned_data.get('google_maps_link', '').strip()
        if '<iframe' in link and 'src="' in link:
            start = link.find('src="') + len('src="')
            end = link.find('"', start)
            link = link[start:end]
        if not link.startswith("https://www.google.com/maps/embed?"):
            raise forms.ValidationError("Please paste a valid Google Maps embed link!")
        return link


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')


class QAForumForm(forms.ModelForm):
    class Meta:
        model = QAForum
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Ask a question or leave a message...',
                'style': 'width: 100%; padding: 10px;',
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Leave a review...',
                'style': 'width: 100%; padding: 10px;',
            }),
        }
