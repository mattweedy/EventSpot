from django.db import models

class Image(models.Model):
    class Meta:
        app_label = 'app'
    url = models.URLField()
    id = models.UUIDField(primary_key=True)

class MaximumTicketPrice(models.Model):
    class Meta:
        app_label = 'app'
    currency = models.CharField(max_length=50)
    major_value = models.CharField(max_length=50)
    value = models.IntegerField()
    display = models.CharField(max_length=50)

class MinimumTicketPrice(models.Model):
    class Meta:
        app_label = 'app'
    currency = models.CharField(max_length=50)
    major_value = models.CharField(max_length=50)
    value = models.IntegerField()
    display = models.CharField(max_length=50)

class TicketAvailability(models.Model):
    class Meta:
        app_label = 'app'
    maximum_ticket_price = models.OneToOneField(MaximumTicketPrice, on_delete=models.CASCADE)
    minimum_ticket_price = models.OneToOneField(MinimumTicketPrice, on_delete=models.CASCADE)
    is_free = models.BooleanField()
    has_bogo_tickets = models.BooleanField()
    has_available_tickets = models.BooleanField()
    is_sold_out = models.BooleanField()

class Tag(models.Model):
    class Meta:
        app_label = 'app'
    prefix = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)
    display_name = models.CharField(max_length=50)
    _type = models.CharField(max_length=50, null=True)

class Address(models.Model):
    class Meta:
        app_label = 'app'
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    localized_address_display = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=50, null=True)
    address_1 = models.CharField(max_length=200)
    address_2 = models.CharField(max_length=200)
    latitude = models.CharField(max_length=50)
    localized_multi_line_address_display = models.TextField()
    localized_area_display = models.CharField(max_length=200)

class PrimaryVenue(models.Model):
    class Meta:
        app_label = 'app'
    _type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    venue_profile_id = models.UUIDField()
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    venue_profile_url = models.URLField()
    id = models.UUIDField(primary_key=True)

class PrimaryOrganizer(models.Model):
    class Meta:
        app_label = 'app'
    _type = models.CharField(max_length=50)
    num_upcoming_events = models.IntegerField()
    name = models.CharField(max_length=50)
    profile_type = models.CharField(max_length=50)
    num_followers = models.IntegerField()
    url = models.URLField()
    twitter = models.URLField(null=True)
    summary = models.TextField(null=True)
    num_saves = models.IntegerField()
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    followed_by_you = models.BooleanField()
    facebook = models.URLField(null=True)
    num_collections = models.IntegerField()
    id = models.UUIDField(primary_key=True)
    website_url = models.URLField(null=True)
    num_following = models.IntegerField()

class Event(models.Model):
    class Meta:
        app_label = 'app'
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    url = models.URLField()
    primary_venue = models.ForeignKey(PrimaryVenue, on_delete=models.CASCADE)
    primary_organizer = models.ForeignKey(PrimaryOrganizer, on_delete=models.CASCADE)
    eventbrite_event_id = models.UUIDField()
    summary = models.TextField(null=True)
    tags = models.ManyToManyField(Tag)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)
    timezone = models.CharField(max_length=50)
    tickets_url = models.URLField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=50)
    _type = models.CharField(max_length=50)
    ticket_availability = models.OneToOneField(TicketAvailability, on_delete=models.CASCADE)
    is_cancelled = models.BooleanField()
    hide_start_date = models.BooleanField()

class Pagination(models.Model):
    class Meta:
        app_label = 'app'
    object_count = models.IntegerField()
    continuation = models.TextField()
    page_count = models.IntegerField()
    page_size = models.IntegerField()
    has_more_items = models.BooleanField()
    page_number = models.IntegerField()

class ResponseModel(models.Model):
    class Meta:
        app_label = 'app'
    pagination = models.OneToOneField(Pagination, on_delete=models.CASCADE)
    events = models.ManyToManyField(Event)