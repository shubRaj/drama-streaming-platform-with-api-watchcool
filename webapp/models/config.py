from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import IntegrityError
from django.utils import timezone
from .movie import Movie
from .tv import Episode
STATUS_CHOICES = (
    ("p", "Pending"),
    ("c", "Cancelled"),
    ("s", "Solved"),
)


class CustomUser(AbstractUser):
    pass


class Configuration(models.Model):
    title = models.CharField(max_length=300)
    favicon = models.ImageField(
        blank=True, null=True, upload_to="images/favicon")
    description = models.TextField(null=True, blank=True)
    custom_header = models.TextField(null=True, blank=True)
    custom_footer = models.TextField(null=True, blank=True)
    themoviedb_api_key = models.CharField(
        max_length=600, null=True, blank=True)
    message_title = models.CharField(max_length=30, null=True, blank=True)
    show_message = models.BooleanField(default=0)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Configuration"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Configuration, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Configuration"


class Report(models.Model):
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="report",
                                related_query_name="has_report", null=True, blank=True, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="report",
                              related_query_name="has_report", null=True, blank=True, editable=False)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="p")
    description = models.TextField()
    added_on = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        if self.episode:
            return self.episode.name
        elif self.movie:
            return self.movie.title
        return ""

    class Meta:
        ordering = ("-added_on",)


class Page(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    order = models.PositiveSmallIntegerField(
        null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = Page.objects.count()+1
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("order",)
