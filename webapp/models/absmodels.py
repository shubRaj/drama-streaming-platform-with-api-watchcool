from django.db import models
import hashlib,datetime
from django.utils.text import slugify
from django.utils import timezone
from django.core.validators import MaxValueValidator
class AbsShow(models.Model):
    themoviedb_id = models.IntegerField(unique=True)
    imdb_id = models.CharField(max_length=13,null=True,blank=True,unique=True)
    original_title = models.CharField(max_length=300,null=True,blank=True)
    featured = models.BooleanField(default=False)
    overview = models.TextField(null=True,blank=True)
    backdrop_path = models.URLField(null=True)
    poster_path = models.URLField(null=True)
    release_date = models.DateField(null=True,blank=True)
    title = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200,blank=True,null=True)
    vote_average = models.DecimalField(decimal_places=1,max_digits=3,null=True,blank=True,default=0.0,validators=[MaxValueValidator(10),])
    runtime = models.IntegerField(null=True,blank=True)
    published = models.BooleanField(default=True)
    trailer = models.URLField(null=True,blank=True)
    slug = models.SlugField(blank=True,null=True,editable=False,unique=True,max_length=300)
    updated_on = models.DateTimeField(default=timezone.now,editable=False)
    added_on = models.DateTimeField(default=timezone.now,editable=False)
    class Meta:
        abstract = True
    def __str__(self):
        return self.title
    def save(self,*args,**kwargs):
        if self.id:
            self.updated_on = timezone.now()
        if not self.slug:
            year = f'-{datetime.datetime.strptime(str(self.release_date),"%Y-%m-%d").year}' if self.release_date else ''
            # added_on_hash = hashlib.md5(str(self.added_on).encode()).hexdigest()
            self.slug = slugify(f"{self.title}-{year}-with-english-subtitle-full-hd")
        super(AbsShow,self).save(*args,**kwargs)
class AbsWatch(models.Model):
    source = models.CharField(max_length=30)
    quality = models.CharField(max_length=30,default="Auto")
    language = models.CharField(max_length=50,default="English")
    url = models.URLField(max_length=2083)
    added_on = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.url
    class Meta:
        abstract = True
class AbsDownload(models.Model):
    original_url = models.URLField(max_length=2083,null=True)
    slug = models.SlugField(max_length=2083,null=True)
    source = models.CharField(max_length=30,null=True)
    added_on = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.source
    class Meta:
        abstract = True
class AbsSubtitle(models.Model):
    url = models.URLField(max_length=2083)
    added_on = models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        return self.url
    class Meta:
        abstract = True