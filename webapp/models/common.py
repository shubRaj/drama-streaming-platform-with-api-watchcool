from django.db import models
from .movie import Movie
from .tv import TV
GENDER_CHOICES = (
    (1,"Female"),
    (0,'Male'),
)
class Genre(models.Model):
    movie = models.ManyToManyField(Movie)
    tv = models.ManyToManyField(TV)
    name = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.name
class Status(models.Model):
    movie = models.ManyToManyField(Movie)
    tv = models.ManyToManyField(TV)
    name = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.name
class Cast(models.Model):
    movie = models.ManyToManyField(Movie)
    tv = models.ManyToManyField(TV)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default=1)
    name = models.CharField(max_length=100)
    tmdb_cast_id = models.IntegerField()
    popularity = models.DecimalField(max_digits=4,decimal_places=3)
    profile_path = models.URLField(null=True,blank=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ("popularity",)