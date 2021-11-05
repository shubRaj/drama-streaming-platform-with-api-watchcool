from django.contrib.sitemaps import Sitemap
from .models import TV,Movie,Episode,Page,Cast
class PageSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5
    protocol = 'https'
    def items(self):
        return Page.objects.all()
class TVDetailSitemap(Sitemap):
    changefreq = 'daily'
    limit = 200
    priority = 0.8
    protocol = 'https'
    def items(self):
        return TV.objects.all()
class MovieDetailSitemap(Sitemap):
    changefreq = 'weekly'
    limit = 200
    priority = 1
    protocol = 'https'
    def items(self):
        return Movie.objects.all()
class EpisodeDetailSitemap(Sitemap):
    changefreq = 'weekly'
    limit = 200
    priority = 1
    protocol = 'https'
    def items(self):
        return Episode.objects.all()
class CastSitemap(Sitemap):
    changefreq = 'weekly'
    limit = 200
    priority = 1
    protocol = 'https'
    def items(self):
        return Cast.objects.all()