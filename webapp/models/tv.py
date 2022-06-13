from .absmodels import AbsShow,AbsWatch,AbsSubtitle,AbsDownload
from django.db import models
import hashlib
import datetime
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
class TV(AbsShow):
    media_type=models.CharField(default="TV",max_length=2)
    class Meta:
        ordering = ("-added_on","-release_date",)
        verbose_name_plural = "TV Shows"
        db_table = "tv"
    def get_absolute_url(self):
        return reverse("app_webapp:tv_detail",args=(self.slug,))
class Type(models.Model):
    tv = models.ManyToManyField(TV,related_name="type",related_query_name="type")
    name = models.CharField(max_length=30,unique=True)
    def __str__(self):
        return self.name
class Season(models.Model):
    tv = models.ForeignKey(TV,on_delete=models.CASCADE,related_name="season",related_query_name="has_season")
    tmdb_season_id = models.IntegerField()
    season_number = models.IntegerField()
    episode_count = models.IntegerField()
    name = models.CharField(max_length=30,null=True,blank=True)
    overview = models.TextField(null=True,blank=True)
    poster_path = models.URLField(null=True,blank=True)
    air_date = models.DateField(null=True,blank=True)
    added_on = models.DateTimeField(default=timezone.now,editable=False)
    updated_on = models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        if not self.name:
            return str(self.season_number)
        return self.name
    class Meta:
        ordering = ("-season_number","-added_on",)
    def save(self,*args,**kwargs):
        if self.id:
            self.updated_on = timezone.now()
        return super().save(*args,**kwargs)
class Episode(models.Model):
    season = models.ForeignKey(Season,on_delete=models.CASCADE,related_name="episode",related_query_name="has_episode")
    name = models.CharField(max_length=100,null=True,blank=True)
    overview = models.TextField(null=True,blank=True)
    episode_number = models.CharField(max_length=6)
    season_number = models.IntegerField()
    tmdb_episode_id = models.IntegerField(null=True,blank=True)
    source_url = models.CharField(null=True,blank=True,max_length=2083)
    slug = models.SlugField(null=True,blank=True,max_length=2083)
    still_path = models.URLField(null=True,blank=True)
    vote_average = models.IntegerField(null=True,blank=True)
    views = models.IntegerField(default=0,editable=False)
    air_date = models.DateField(null=True,blank=True)
    added_on = models.DateTimeField(default=timezone.now,editable=False)
    updated_on = models.DateTimeField(default=timezone.now,editable=False)
    class Meta:
        ordering = ("-episode_number","-added_on",)
    def get_absolute_url(self):
        return reverse("app_webapp:watch_episode",args=(self.slug,))
    def __str__(self):
        if not self.name:
            return str(self.episode_number)
        return self.name
    def save(self, *args,**kwargs):
        if self.still_path and self.still_path.startswith("/"):
            self.still_path = f"https://www.themoviedb.org/t/p/original{self.still_path}"
        if self.id:
            self.updated_on = self.season.updated_on =timezone.now() 
        if not self.slug:
            # added_on_hash = hashlib.md5(str(self.added_on).encode()).hexdigest()
            year = f'-{datetime.datetime.strptime(str(self.season.tv.release_date),"%Y-%m-%d").year}' if self.season.tv.release_date else ''
            self.slug = slugify(f"{self.season.tv.title}{year}-season-{self.season.season_number}-episode-{self.episode_number}")
        super(Episode,self).save(*args,**kwargs)
class WatchEpisode(AbsWatch):
    episode = models.ForeignKey(Episode,on_delete=models.CASCADE,related_name="watch_episode",related_query_name="has_watch_episode")
    class Meta:
        db_table = "watch_episode"
        verbose_name_plural = "WatchEpisodes"
class DownloadEpisode(AbsDownload):
    episode = models.ForeignKey(Episode,on_delete=models.CASCADE,related_name="download_episode",related_query_name="has_download_episode")
    class Meta:
        db_table = "download_episode"
        verbose_name_plural = "DownloadEpisodes"

class EpisodeSubtitle(AbsSubtitle):
    episode = models.ForeignKey(Episode,on_delete=models.CASCADE,related_name="episode_subtitle",related_query_name="has_episode_subtitle")
    class Meta:
        db_table = "episode_subtitle"
        verbose_name_plural = "EpisodeSubtitles"