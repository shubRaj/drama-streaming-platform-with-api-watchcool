from django.db import models
from django.utils import timezone
DOWNLOAD_OPTIONS = (
    ("Free","Free"),
    ("WithAdsUnlock","WithAdsUnlock"),
    ("PremiumOnly","PremiumOnly")
)
def default_tmdb_lang():
    return {"english_name":"English","iso_639_1":"en","name":"English"}
class Configuration(models.Model):
    app_name = models.CharField(max_length=40)
    authorization = models.CharField(max_length=191,null=True,blank=True)
    tmdb_api_key = models.CharField(max_length=191,default="9f002d3cbd8d807b5af7339bf13b63fd")
    purchase_key = models.CharField(max_length=191,null=True,blank=True,default="5f107d7d-e117-4858-9dde-8f5eb5839dfd")
    tmdb_lang = models.JSONField(default=default_tmdb_lang)
    app_url_android = models.URLField(null=True,blank=True)
    autosubstitles = models.BooleanField(default=False)
    livetv = models.BooleanField(default=False)
    streaming = models.BooleanField(default=False)
    ads_player = models.BooleanField(default=False)
    anime = models.BooleanField(default=False)
    facebook_show_interstitial = models.PositiveSmallIntegerField(default=0)
    ad_show_interstitial = models.PositiveSmallIntegerField(default=0)
    ad_interstitial = models.PositiveSmallIntegerField(default=0)
    ad_unit_id_interstitial = models.CharField(max_length=191,null=True,blank=True)
    ad_banner = models.BooleanField(default=False)
    ad_unit_id_banner = models.CharField(max_length=191,null=True,blank=True)
    ad_face_audience_interstitial = models.PositiveSmallIntegerField(default=0)
    ad_face_audience_banner = models.PositiveIntegerField(default=0)
    ad_unit_id_facebook_interstitial_audience=models.CharField(max_length=191,null=True,blank=True)
    ad_unit_id_facebook_banner_audience = models.CharField(max_length=191,null=True,blank=True)
    privacy_policy = models.TextField(null=True,blank=True)
    latestVersion = models.CharField(max_length=4,blank=True,null=True)
    update_title = models.CharField(max_length=40,blank=True,null=True)
    releaseNotes = models.TextField(null=True,blank=True)
    enable_custom_message = models.BooleanField(default=False)
    custom_message = models.TextField(null=True,blank=True)
    url = models.URLField(null=True,blank=True)
    imdb_cover_path = models.URLField(default="http://image.tmdb.org/t/p/w500")
    featured_home_numbers= models.IntegerField(default=5)
    next_episode_timer = models.PositiveSmallIntegerField(default=10)
    facebook_url = models.URLField(null=True,blank=True)
    twitter_url = models.URLField(null=True,blank=True)
    instagram_url =models.URLField(null=True,blank=True)
    telegram_url = models.URLField(null=True,blank=True)
    media_placehoder_path = models.CharField(max_length=100,null=True,blank=True)
    server_choices = models.BooleanField(default=False)
    download_premium_only = models.BooleanField(default=False)
    default_downloads_options = models.CharField(max_length=13,choices=DOWNLOAD_OPTIONS,default="Free")
    wach_ads_to_unlock_player = models.BooleanField(default=False)
    enable_custom_banner = models.BooleanField(default=False)
    custom_banner_image = models.ImageField(upload_to="custom_banner",null=True,blank=True)
    custom_banner_link = models.URLField(null=True,blank=True)
    maintenance_mode = models.BooleanField(default=False)
    mantenance_mode_message = models.TextField(null=True,blank=True)
    splash_image = models.URLField(null=True,blank=True)
    allow_adm = models.BooleanField(default=False) 
    default_youtube_quality  = models.CharField(null=True,blank=True,max_length=20)
    enable_previews = models.BooleanField(default=False)
    enable_pinned = models.BooleanField(default=False)
    enable_vlc = models.BooleanField(default=False)
    resume_offline  = models.BooleanField(default=True)
    user_agent =  models.CharField(max_length=100,blank=True,null=True)
    enable_upcoming = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now,editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    def save(self,*args,**kwargs):
        if self.id:
            self.updated_at = timezone.now()
            self.id = 1
        return super().save(*args,**kwargs)
    class Meta:
        verbose_name_plural="Android Configuration"