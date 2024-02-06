from django.db import models

class Events(models.Model):
    event_name = models.CharField(max_length=100)
    event_genre = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.TimeField()
    event_location = models.CharField(max_length=100)
    event_description = models.TextField()
    event_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.event_name