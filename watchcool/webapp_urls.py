from .urls import urlpatterns
from django.contrib.sitemaps import views as sitemap_views
from django.urls import path,include
from webapp.sitemaps import PageSitemap,TVDetailSitemap,MovieDetailSitemap,EpisodeDetailSitemap,CastSitemap
sitemaps = {
    "pages":PageSitemap,
    "tv-show-detail":TVDetailSitemap,
    "movie-detail":MovieDetailSitemap,
    "episode-detail":EpisodeDetailSitemap,
    "cast":CastSitemap,
}
urlpatterns.extend(
    [
        path("watchdog.xml",sitemap_views.index,{"sitemaps":sitemaps},name="django.contrib.sitemaps.views.sitemap"),
        path('watchdog-<section>.xml', sitemap_views.sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
        path("api/",include("appapi.urls",namespace="appapi")),
        path("",include("webapp.urls",namespace="webapp")),
    ]
)