from django.db import models
from django.utils import timezone
class AbsShow(models.Model):
    themoviedb_id = models.IntegerField(unique=True)
    imdb_id = models.IntegerField(null=True,blank=True,unique=True)
    original_title = models.CharField(max_length=300,null=True,blank=True)
    overview = models.TextField(null=True)
    backdrop_path = models.URLField(null=True)
    poster_path = models.URLField(null=True)
    release_date = models.DateField(null=True,blank=True)
    title = models.CharField(max_length=30)
    tagline = models.CharField(max_length=200,blank=True,null=True)
    vote_average = models.DecimalField(decimal_places=1,max_digits=3,null=True,blank=True,default=0.0)
    published = models.BooleanField(default=True)
    views = models.IntegerField(default=0,editable=False)
    added_on = models.DateTimeField(default=timezone.now,editable=False)
    class Meta:
        ordering = ("added_on","-release_date",)
        abstract = True
    def __str__(self):
        return self.title
class AbsWatch(models.Model):
    source = models.CharField(max_length=30)
    url = models.URLField(max_length=2083)
    is_downloadable = models.BooleanField(default=False,verbose_name="downloadable")
    added_on = models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        return self.url
    class Meta:
        abstract = True
class AbsSubtitle(models.Model):
    url = models.URLField(max_length=2083)
    added_on = models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        return self.url
    class Meta:
        abstract = True