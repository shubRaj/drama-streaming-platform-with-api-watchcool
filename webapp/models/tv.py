from .absmodels import AbsShow,AbsWatch,AbsSubtitle
from django.db import models
class TV(AbsShow):
    class Meta:
        verbose_name_plural = "TV Shows"
        db_table = "tv"
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
    air_date = models.DateTimeField(null=True,blank=True)
    def __str__(self):
        if not self.name:
            return str(self.season_number)
        return self.name
    class Meta:
        ordering = ('-air_date',)
class Episode(models.Model):
    season = models.ForeignKey(Season,on_delete=models.CASCADE,related_name="season",related_query_name="has_season")
    name = models.CharField(max_length=10,null=True,blank=True)
    overview = models.TextField(null=True,blank=True)
    episode_number = models.IntegerField()
    season_number = models.IntegerField()
    tmdb_episode_id = models.IntegerField()
    trailer = models.URLField(null=True,blank=True)
    still_path = models.URLField(null=True,blank=True)
    vote_average = models.IntegerField(null=True,blank=True)
    views = models.IntegerField(default=0,editable=False)
    air_date = models.DateTimeField(null=True,blank=True)
    class Meta:
        ordering = ('-air_date',)
    def __str__(self):
        if not self.name:
            return str(self.episode_number)
        return self.name
    def save(self, *args,**kwargs):
        if self.still_path and self.still_path.startswith("/"):
            self.still_path = f"https://www.themoviedb.org/t/p/original{self.still_path}"
        super(Episode,self).save(*args,**kwargs)
class WatchEpisode(AbsWatch):
    episode = models.ForeignKey(Episode,on_delete=models.CASCADE,related_name="watch_episode",related_query_name="has_watch_episode")
    class Meta:
        db_table = "watch_episode"
        verbose_name_plural = "WatchEpisodes"
class EpisodeSubtitle(AbsSubtitle):
    episode = models.ForeignKey(Episode,on_delete=models.CASCADE,related_name="episode_subtitle",related_query_name="has_episode_subtitle")
    class Meta:
        db_table = "episode_subtitle"
        verbose_name_plural = "EpisodeSubtitles"