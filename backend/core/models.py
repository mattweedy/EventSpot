from django.db import models
from django.utils import timezone

class Venue(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    venue_id = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    event_id = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    venue_id = models.ForeignKey(Venue, on_delete=models.CASCADE)
    image = models.URLField()
    tags = models.CharField(max_length=255)
    tickets_url = models.URLField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    summary = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.date < timezone.now().date():
            self.status = 'past'
        else:
            self.status = 'upcoming'
        super().save(*args, **kwargs)