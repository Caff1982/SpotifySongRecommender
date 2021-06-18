from django.db import models


class Song(models.Model):
    """
    Stores each row of the dataset as an individual song.

    song_id: The Spotify song ID
    is_major: True if song is in major key, False for minor
    """
    song_id = models.CharField(max_length=30)
    name = models.CharField(max_length=500)
    artist = models.CharField(max_length=800)
    popularity = models.IntegerField()
    duration_ms = models.IntegerField()
    is_explicit = models.BooleanField(default=False)
    release_year = models.IntegerField()
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.IntegerField()
    loudness = models.FloatField()
    is_major = models.BooleanField(default=True)
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    time_signature = models.IntegerField()

    def __str__(self):
        return f'{self.artist}: {self.name}'
 



