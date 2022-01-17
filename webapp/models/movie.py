from django.db import models
from django.urls import reverse
from .absmodels import AbsWatch,AbsSubtitle,AbsShow,AbsDownload
class Movie(AbsShow):
    media_type=models.CharField(default="MOVIE",max_length=5)
    source_url = models.CharField(null=True,blank=True,max_length=2083)
    class Meta:
        ordering = ("-added_on","-release_date",)
        db_table = "movie"
    def get_absolute_url(self):
        return reverse("app_webapp:movie_detail",args=(self.slug,))
class WatchMovie(AbsWatch):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="watch",related_query_name="has_watch",editable=False)
    class Meta:
        db_table = "watch_movie"
        verbose_name_plural = "WatchMovies"
class DownloadMovie(AbsDownload):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="download",related_query_name="has_download",editable=False)
    class Meta:
        db_table = "download_movie"
        verbose_name_plural = "DownloadMovies"
class MovieSubtitle(AbsSubtitle):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="subtitle",related_query_name="has_subtitle",editable=False)
    class Meta:
        db_table = "movie_subtitle"
        verbose_name_plural = "MovieSubtitles"