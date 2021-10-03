from django.utils import timezone
from django.db import models
from .absmodels import AbsWatch,AbsSubtitle,AbsShow
class Movie(AbsShow):
    trailer = models.URLField(null=True,blank=True)
    runtime = models.IntegerField(null=True,blank=True)
    class Meta:
        db_table = "movie"
class WatchMovie(AbsWatch):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="watch",related_query_name="has_watch")
    class Meta:
        db_table = "watch_movie"
        verbose_name_plural = "WatchMovies"
class MovieSubtitle(AbsSubtitle):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="subtitle",related_query_name="has_subtitle",editable=False)
    class Meta:
        db_table = "movie_subtitle"
        verbose_name_plural = "MovieSubtitles"