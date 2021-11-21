"""watchcool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps import views as sitemap_views
from webapp.sitemaps import PageSitemap,TVDetailSitemap,MovieDetailSitemap,EpisodeDetailSitemap,CastSitemap
sitemaps = {
    "pages":PageSitemap,
    "tv-show-detail":TVDetailSitemap,
    "movie-detail":MovieDetailSitemap,
    "episode-detail":EpisodeDetailSitemap,
    "cast":CastSitemap,
}
urlpatterns = [
    path('logmein/', admin.site.urls,name="logmein"),
    path('dashboard/',include("adminDashboard.urls",namespace="adminDashboard")),
    path("",include("appapi.urls",namespace="appapi")),
    # path("watchdog.xml",sitemap_views.index,{"sitemaps":sitemaps},name="django.contrib.sitemaps.views.sitemap"),
    # path('watchdog-<section>.xml', sitemap_views.sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    path("web16/",include("webapp.urls",namespace="webapp")),
]
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    handler404 = "webapp.handlers.page_not_found"
    handler500 = "webapp.handlers.server_error"
    handler400 = "webapp.handlers.bad_request"