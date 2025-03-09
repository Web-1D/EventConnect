"""
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Copied from tangowithdjango, think username and password stored in form.py in rango
class UserProfile(models.Model):
    user = models.ManyToManyField(User, on_delete=models.CASCADE)

    #website = models.URLField(blank=True)
    #picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
class Event(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    organiser_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name
"""


