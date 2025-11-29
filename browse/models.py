from django.db import models

# Create your models here.
class Movie(models.Model):
    poster_path=models.CharField(null=True, max_length=50)
    tmdb_id = models.CharField(null=True, max_length=250)
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(null=True)
    vote_average = models.FloatField(blank=True)
    language = models.CharField(max_length=10)
    popularity = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)

    def __str__(self):
        return self.title
    
    

