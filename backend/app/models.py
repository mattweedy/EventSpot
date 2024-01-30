from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    # add more as needed

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    genre = models.CharField(max_length=100)
    # add more as needed