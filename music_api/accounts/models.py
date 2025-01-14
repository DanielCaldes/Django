from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.username

class FavouriteArtist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favourite_artists")
    artist_id = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('user', 'artist_id')

class FavouriteTrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favourite_tracks")
    track_id = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'track_id')