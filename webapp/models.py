from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('organiser', 'Organiser'),
    ]

    email = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    groups = None
    user_permissions = None

    def __str__(self):
        return f"{self.username} ({self.role})"

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
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    comment = models.TextField()
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.event.title}'

class QAForum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Message by {self.user.username} at {self.timestamp}'



