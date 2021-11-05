from django.db import models
from .movie import Movie
from .tv import TV
from django.contrib.auth import get_user_model
import hashlib
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
import random
GENDER_CHOICES = (
    ("1","Female"),
    ("2",'Male'),
)
USER = get_user_model()
def generateRandomColor():
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
    return color[0]
class Genre(models.Model):
    movie = models.ManyToManyField(Movie,related_name="genre",related_query_name="has_genre")
    tv = models.ManyToManyField(TV,related_name="genre",related_query_name="has_genre")
    name = models.CharField(max_length=20,unique=True)
    color = models.CharField(max_length=9,null=True,blank=True,default=generateRandomColor,editable=True)
    def __str__(self):
        return self.name
class Language(models.Model):
    movie = models.ManyToManyField(Movie,related_name="language",related_query_name="has_language")
    tv = models.ManyToManyField(TV,related_name="language",related_query_name="has_language")
    name = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.name
class Status(models.Model):
    movie = models.ManyToManyField(Movie,related_name="status",related_query_name="has_status")
    tv = models.ManyToManyField(TV,related_name="status",related_query_name="has_status")
    name = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Status"
class Cast(models.Model):
    movie = models.ManyToManyField(Movie,related_name="cast",related_query_name="has_cast")
    tv = models.ManyToManyField(TV,related_name="cast",related_query_name="has_cast")
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default=1)
    name = models.CharField(max_length=100)
    tmdb_cast_id = models.IntegerField()
    popularity = models.DecimalField(max_digits=6,decimal_places=3,null=True,blank=True)
    profile_path = models.URLField(null=True,blank=True)
    slug = models.SlugField(null=True,blank=True,editable=True,max_length=2083)
    added_on = models.DateField(default=timezone.now,editable=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ("-popularity",)
    def save(self,*args,**kwargs):
        if not self.slug:
            tmdb_cast_id_hash = hashlib.md5(str(self.tmdb_cast_id).encode()).hexdigest()
            self.slug = slugify(f"{self.name}-{tmdb_cast_id_hash}")
        return super(Cast,self).save(*args,**kwargs)
    def get_absolute_url(self):
        return reverse("app_webapp:actor_detail",args=(self.slug,))
class Review(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="review",related_query_name="has_review",null=True,blank=True)
    tv = models.ForeignKey(TV,on_delete=models.CASCADE,related_name="review",related_query_name="has_review",null=True,blank=True)
    user = models.ForeignKey(USER,on_delete=models.CASCADE,related_name="review",related_query_name="has_review",null=True,blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3,decimal_places=1,default=0.0)
    approved = models.BooleanField(default=False)
    added_on = models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        return self.title
    def show(self):
        return self.tv or self.movie
    class Meta:
        ordering = ("-added_on",)
class ViewLog(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="view",related_query_name="has_view",null=True,blank=True,db_column="movie")
    tv = models.ForeignKey(TV,on_delete=models.CASCADE,related_name="view",related_query_name="has_view",null=True,blank=True,db_column="tv")
    user = models.ForeignKey(USER,on_delete=models.SET_NULL,related_name="view",related_query_name="has_view",null=True,blank=True,db_column="user")
    viewed_on = models.DateTimeField(default=timezone.now,editable=False,db_column="viewed_on")
    def __str__(self):
        return str(self.movie or self.tv)
    class Meta:
        db_table = "viewlog"
        verbose_name_plural = "ViewLogs"
        ordering = ("-viewed_on",)