from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.username

class FavouriteArtist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favourite_artists")
    spotify_artist_id = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('user', 'spotify_artist_id')

class FavouriteTrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favourite_tracks")
    spotify_track_id = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'spotify_track_id')