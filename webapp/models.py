from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('organiser', 'Organiser'),
    ]

    email = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    groups = None
    user_permissions = None

    def __str__(self):
        return f"{self.username} ({self.role})"

    def is_organiser(self):
        return self.role == 'organiser'


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    organiser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organised_events')
    attendees = models.ManyToManyField(User, related_name='attended_events', blank=True)
    google_maps_link = models.TextField(
        blank=True,
        null=True,
    )

    def clean(self):
        if '<iframe' in self.location:
            match = re.search(r'src="([^"]+)"', self.location)
            if match:
                self.location = match.group(1)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.event.title}"


class QAForum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username} at {self.timestamp}"


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    message = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"To {self.recipient.username} from {self.sender.username}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.event.title}"
