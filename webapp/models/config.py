from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import IntegrityError
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from .movie import Movie
from .tv import Episode
STATUS_CHOICES = (
    ("p", "Pending"),
    ("c", "Cancelled"),
    ("s", "Solved"),
)
OPTIONS = (
    ("1", "The video is not opening"),
    ("2", "Subtitle has character issues"),
    ("3", "Other"),
)

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20,null=True,blank=True)
    last_name = models.CharField(max_length=20,null=True,blank=True)
    username = models.CharField(max_length=64,null=True,blank=True)
    profile = models.ImageField(upload_to="profiles",default="profiles/user.png",null=True,blank=True)
    approved = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=30,null=True,blank=True,editable=False)
    def __str__(self):
        return self.username
    class Meta:
        ordering = ("-date_joined",)
        verbose_name_plural = "Users"

class Configuration(models.Model):
    title = models.CharField(max_length=300)
    favicon = models.ImageField(
        blank=True, null=True, upload_to="images")
    logo = models.ImageField(
        blank=True, null=True, upload_to="images")
    tagline = models.CharField(null=True,blank=True,max_length=200)
    description = models.TextField(null=True, blank=True)
    custom_header = models.TextField(null=True, blank=True)
    custom_footer = models.TextField(null=True, blank=True)
    themoviedb_api_key = models.CharField(
        max_length=600, null=True, blank=True)
    gdplayer_auth = models.CharField(max_length=120,null=True, blank=True)
    recaptcha_site_key = models.CharField(max_length=40,null=True)
    recaptcha_secret_key = models.CharField(max_length=40,null=True)
    app_url = models.URLField(null=True,blank=True)
    show_message = models.BooleanField(default=False)
    message_title = models.CharField(max_length=30, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    movie_comment = models.BooleanField(default=False)
    tv_comment = models.BooleanField(default=False)

    def __str__(self):
        return "Configuration"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Configuration, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Configuration"


class Report(models.Model):
    title = models.CharField(max_length=300,null=True,blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="p")
    option = models.CharField(
        max_length=50, choices=OPTIONS, default="1")
    description = models.TextField(null=True,blank=True)
    added_on = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.title or ""

    class Meta:
        ordering = ("-added_on",)


class Page(models.Model):
    title = models.CharField(max_length=30,unique=True)
    description = models.TextField()
    order = models.PositiveSmallIntegerField(
        null=True, blank=True, unique=True)
    slug = models.SlugField(max_length=50,null=True,blank=True,editable=False)
    def save(self, *args, **kwargs):
        if not self.order:
            self.order = Page.objects.count()+1
        if not self.slug:
            self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("app_webapp:page",args=(self.slug,))
    def __str__(self):
        return self.title

    class Meta:
        ordering = ("order",)