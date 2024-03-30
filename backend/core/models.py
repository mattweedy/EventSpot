from django.db import models
from django.utils import timezone
# from django.core.cache import cache
# from django.apps import apps

genre_dict = {
    "techno": ["techno", "electronic", "edm", "dance", "rave"],
    "rave": ["rave", "electronic", "edm", "techno", "dance"],
    "house": ["house", "electronic", "edm", "dance", "rave"],
    "trance": ["trance", "electronic", "edm", "dance", "rave"],
    "dubstep": ["dubstep", "electronic", "edm", "dance"],
    "drum and bass": ["drum and bass", "electronic", "edm", "dance", "rave"],
    "gabber": ["gabber", "electronic", "edm", "dance"],
    "hardgroove": ["hardgroove", "electronic", "dance", "techno", "rave"],
    "hardstyle": ["hardstyle", "electronic", "edm", "dance", "techno", "rave"],
    "psytrance": ["psytrance", "electronic", "edm", "dance", "trance"],
    "synthpop": ["synthpop", "grunge", "alternative", "indie"],
    "trap": ["trap", "rap", "hip hop", "street"],
    "hip hop": ["hip hop", "rap", "street"],
    "hiphop": ["hip hop", "rap", "street"],
    "rap": ["rap", "hip hop", "street"],
    "pop": ["pop", "dance"],
    "dance": ["pop", "dance"],
    "rock": ["rock", "metal"],
    "metal": ["rock", "metal", "hard rock"],
    "hard rock": ["rock", "metal", "hard rock"],
    "country": ["country", "bluegrass"],
    "bluegrass": ["country", "bluegrass"],
    "jazz": ["jazz", "blues"],
    "blues": ["jazz", "blues"],
    "classical": ["classical", "orchestral"],
    "orchestral": ["classical", "orchestral"],
    "electronic": ["electronic", "edm", "dance"],
    "edm": ["electronic", "edm", "dance"],
    "indie": ["indie", "alternative"],
    "alternative": ["indie", "alternative"],
    "folk": ["folk", "acoustic"],
    "acoustic": ["folk", "acoustic"],
    "r&b": ["r&b", "soul"],
    "soul": ["r&b", "soul"],
    "reggae": ["reggae", "ska"],
    "ska": ["reggae", "ska"],
    "punk": ["punk", "emo"],
    "emo": ["punk", "emo"],
    "latin": ["latin", "salsa"],
    "salsa": ["latin", "salsa"],
    "gospel": ["gospel", "spiritual"],
    "spiritual": ["gospel", "spiritual"],
    "funk": ["funk", "disco"],
    "disco": ["funk", "disco"],
    "world": ["world", "international"],
    "international": ["world", "international"],
    "new age": ["new age", "ambient"],
    "ambient": ["new age", "ambient"],
    "soundtrack": ["soundtrack", "score"],
    "score": ["soundtrack", "score"],
    "comedy": ["comedy", "parody"],
    "parody": ["comedy", "parody"],
    "spoken word": ["spoken word", "audiobook"],
    "audiobook": ["spoken word", "audiobook"],
    "children's": ["children's", "kids"],
    "kids": ["children's", "kids"],
    "holiday": ["holiday", "christmas"],
    "christmas": ["holiday", "christmas"],
    "easy listening": ["easy listening", "mood"],
    "mood": ["easy listening", "mood"],
    "brazilian": ["brazilian", "samba"],
    "samba": ["brazilian", "samba"],
    "fado": ["fado", "portuguese"],
    "portuguese": ["fado", "portuguese"],
    "tango": ["tango", "argentinian"],
}

def add_genres(genre_list):
    """
    Add more genres to the genre list.
    """
    new_genre_list = genre_list.copy()
    for genre, add_genres in genre_dict.items():
        for existing_genre in new_genre_list:
            if genre in existing_genre:
                for add_genre in add_genres:
                    if add_genre not in new_genre_list:
                        new_genre_list.append(add_genre)
    return new_genre_list


class Event(models.Model):
    class Meta:
        app_label = "backend"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    event_id = models.CharField(max_length=500, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    venue_id = models.IntegerField()
    venue_identifier = models.CharField(max_length=500, null=True, blank=True)
    image = models.URLField(max_length=500)
    tags = models.CharField(max_length=500)
    tickets_url = models.URLField(max_length=500)
    date = models.CharField(max_length=500)
    summary = models.TextField(max_length=500, blank=True, null=True)

    @classmethod
    def create_from_event_and_venue(cls, event, venue):
        event['tags'] = [tag['display_name'].lower() for tag in event['tags']]

        # Add more genres to the event
        event['tags'] = add_genres(event['tags'])

        # Filter out events related to kids
        kids_words = ['kids', 'child', 'children', 'baby', 'babies', 'toddler']
        if any(kid_word in event['name'].lower() or kid_word in ' '.join(event['tags']) for kid_word in kids_words):
            return None

        name = event["name"]
        event_id = event["eventbrite_event_id"]
        price = event["ticket_availability"]["minimum_ticket_price"]["major_value"]
        venue_id = venue.id
        venue_identifier = venue.venue_id
        image = event["image"]["url"]
        # tags = ','.join(tag['display_name'].lower() for tag in event['tags'])
        tags = ','.join(event['tags'])
        tickets_url = event["tickets_url"]
        date = event["start_date"]
        summary = event["summary"]

        # create or update the event
        event_insert, created = cls.objects.update_or_create(
            event_id=event["eventbrite_event_id"],
            defaults={
                'name': name,
                'event_id': event_id,
                'price': price,
                'venue_id': venue_id, # this should be Venue.venue_id pretty much
                'venue_identifier': venue_identifier,
                'image': image,
                'tags': tags,
                'tickets_url': tickets_url,
                'date': date,
                'summary': summary
            },
        )
        if created:
            print("A new event was created.")
        else:
            print("An existing event was updated.")

        return event_insert
    
    def __str__(self):
        return (
            f"------------------------\n"
            f"EVENT   : {self.name}\n"
            f"ID      : {self.event_id}\n"
            f"PRICE   : {self.price}\n"
            f"DATE    : {self.date}\n"
            f"SUMMARY : {self.summary}\n"
            f"------------------------"
        )


class Venue(models.Model):
    # Track = apps.get_model("backend", "Track")
    # Artist = apps.get_model("backend", "Artist")
    
    class Meta:
        app_label = "backend"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    venue_id = models.CharField(max_length=1000, unique=True)
    address = models.CharField(max_length=1000)
    city = models.CharField(max_length=1000)
    country = models.CharField(max_length=1000)

    @classmethod
    def create_from_event(cls, event):
        venue = event["primary_venue"]
        address = venue["address"]
        
        # extract information from event
        name = venue["name"].replace("'", "")
        venue_id = event['primary_venue_id']
        localised_addr = address["localized_address_display"]
        city = address["region"]
        country = address["country"]
        
        # create or update the Venue
        venue, created = cls.objects.update_or_create(
            name=name,
            defaults={
                'venue_id': venue_id,
                'address': localised_addr,
                'city': city,
                'country': country 
            },
        )
        if created:
            print("A new venue was created.")
        else:
            print("An existing venue was updated.")

        return venue
    
    def __str__(self):
        return (
            f"------------------------\n"
            f"VENUE   : {self.name}\n"
            f"ID      : {self.venue_id}\n"
            f"ADDRESS : {self.address}\n"
            f"CITY    : {self.city}\n"
            f"COUNTRY : {self.country}"
            f"\n------------------------"
        )
    

class User(models.Model):
    class Meta:
        app_label = "backend"

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    venue_preferences = models.TextField(null=True)
    genre_preferences = models.TextField(null=True)
    price_range = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    # recommended_events = models.TextField(null=True)
    recommended_events = models.TextField(default='')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    is_active = models.BooleanField(default=True)

    @classmethod
    def create_user(cls, username, email):
        user, created = cls.objects.update_or_create(
            email=email,
            defaults={
                'username': username,
                'email': email,
            },
        )
        if created:
            print("A new user was created.")
        else:
            print("An existing user was updated.")

        return user
    
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username

    def __str__(self):
        return (
            f"------------------------\n"
            f"USERNAME : {self.username}\n"
            f"EMAIL    : {self.email}\n"
            f"CREATED  : {self.created_at}\n"
            f"UPDATED  : {self.updated_at}"
            f"\n------------------------"
        )