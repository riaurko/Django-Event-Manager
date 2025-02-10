from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=75)
    category = models.ForeignKey('Category', related_name='events', on_delete=models.CASCADE)

class Participant(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField(Event, related_name='participants')

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=150)