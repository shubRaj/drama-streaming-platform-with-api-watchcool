from django.db import models
from .movie import Movie
from .tv import TV
from django.contrib.auth import get_user_model
from django.utils import timezone
GENDER_CHOICES = (
    (1,"Female"),
    (0,'Male'),
)
USER = get_user_model()
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
    class Meta:
        verbose_name_plural = "Status"
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
class Review(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="review",related_query_name="has_review",null=True,blank=True)
    tv = models.ForeignKey(TV,on_delete=models.CASCADE,related_name="review",related_query_name="has_review",null=True,blank=True)
    user = models.ForeignKey(USER,on_delete=models.CASCADE,related_name="review",related_query_name="has_review",null=True,blank=True)
    description = models.TextField()
    rate = models.DecimalField(max_digits=3,decimal_places=1,default=0.0)
    added_on = models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ("-added_on",)