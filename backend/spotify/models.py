# from django.db import models

# class Track(models.Model):
#     class Meta:
#         app_label = "backend"

#     name = models.CharField(max_length=200)
#     spotify_id = models.CharField(max_length=200)
#     artist = models.CharField(max_length=200)
#     genres = models.CharField(max_length=200)
#     popularity = models.IntegerField()

#     def __str__(self):
#         return (
#             f"------------------------\n"
#             f"TRACK      : {self.name}\n"
#             f"ID         : {self.spotify_id}\n"
#             f"ARTIST     : {self.artist}\n"
#             f"GENRES     : {self.genres}\n"
#             f"POPULARITY : {self.popularity}"
#             f"\n------------------------"
#         )
    
    
# class Artist(models.Model):
#     class Meta:
#         app_label = "backend"

#     name = models.CharField(max_length=200)
#     spotify_id = models.CharField(max_length=200)
#     genres = models.CharField(max_length=200)
#     link = models.CharField(max_length=200)
#     popularity = models.IntegerField()

#     def __str__(self):
#         return (
#             f"------------------------\n"
#             f"ARTIST     : {self.name}\n"
#             f"ID         : {self.spotify_id}\n"
#             f"GENRES     : {self.genres}\n"
#             f"LINK       : {self.link}\n"
#             f"POPULARITY : {self.popularity}"
#             f"\n------------------------"
#         )
