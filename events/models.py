from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    thumb = models.ImageField(upload_to='events_thumbnail', default="events_thumbnail/default_thumb.jpg", blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=75)
    category = models.ForeignKey('Category', related_name='events', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='rsvp_events')

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=150)
