from django.db import models

# example user and event models
class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    # add more as needed

class Event(models.Model):
    name = models.CharField(max_length=200)
    venue = models.CharField(max_length=200)
    date = models.DateTimeField()
    price = models.CharField(max_length=50)
    genre = models.CharField(max_length=100)
    # add more as needed