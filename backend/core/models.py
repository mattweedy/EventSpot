from typing import Any
from django.db import models
from django.utils import timezone

class Event(models.Model):
    class Meta:
        app_label = "core"

    def __init__(self, event : list, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.name = event["name"]
        self.event_id = event["eventbrite_event_id"]
        self.price = event["ticket_availability"]["minimum_ticket_price"]["major_value"]
        self.image = event["image"]["url"]
        self.tags = ','.join(tag['display_name'] for tag in event['tags'])
        self.tickets_url = event["tickets_url"]
        self.date = event["start_date"]
        self.summary = event["summary"]
        self.status = "upcoming"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    event_id = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    venue = models.ForeignKey("Venue", on_delete=models.CASCADE)
    image = models.URLField()
    tags = models.CharField(max_length=255)
    tickets_url = models.URLField()
    date = models.DateField()
    summary = models.TextField(blank=True, null=True)


class Venue(models.Model):
    class Meta:
        app_label = "core"
        
    def __init__(self, event, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        venue = event["primary_venue"]
        address = venue["address"]
        self.name = venue["name"]
        self.venue_id = venue["id"]
        self.address = address["localized_address_display"]
        self.city = address["region"]
        self.country = address["country"]

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    venue_id = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)