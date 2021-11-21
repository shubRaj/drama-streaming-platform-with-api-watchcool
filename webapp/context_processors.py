from .models import Configuration,Genre,ViewLog,TV,Page
import datetime
from itertools import chain
from django.db.models import Count,F
from django.core.cache import cache
from django.conf import settings
def moviesViewin(days,get):
    return ViewLog.objects.filter(tv=None,viewed_on__date__gte=(datetime.date.today()-datetime.timedelta(days=days))).values(
        "movie",
        slug=F("movie__slug"),
        title=F("movie__title"),
        themoviedb_id = F("movie__themoviedb_id"),
        original_title = F("movie__original_title"),
        imdb_id = F("movie__imdb_id"),
        trailer = F("movie__trailer"),
        published = F("movie__published"),
        runtime = F("movie__runtime"),
        added_on = F("movie__added_on"),
        updated_on = F("movie__updated_on"),
        media_type = F("movie__media_type"),
        poster_path=F("movie__poster_path"),
        overview=F("movie__overview"),
        vote_average=F("movie__vote_average"),
        backdrop_path=F("movie__backdrop_path"),
        release_date=F("movie__release_date"),
        ).annotate(views=Count("movie")).order_by()[:get]
def tvsViewin(days,get):
    return ViewLog.objects.filter(movie=None,
        viewed_on__date__gte=(datetime.date.today()-datetime.timedelta(days=days))).values(
        "tv",
        slug = F("tv__slug"),
        title=F("tv__title"),
        themoviedb_id = F("tv__themoviedb_id"),
        original_title = F("tv__original_title"),
        imdb_id = F("tv__imdb_id"),
        trailer = F("tv__trailer"),
        published = F("tv__published"),
        runtime = F("tv__runtime"),
        added_on = F("tv__added_on"),
        updated_on = F("tv__updated_on"),
        media_type = F("tv__media_type"),
        poster_path=F("tv__poster_path"),
        overview=F("tv__overview"),
        vote_average=F("tv__vote_average"),
        backdrop_path=F("tv__backdrop_path"),
        release_date=F("tv__release_date"),
        ).annotate(views=Count("tv")).order_by()[:get]
def cache_context():
    data = {}
    config = Configuration.objects.filter(id=1)
    if config.exists():
        config = config.first()
        data["title"] = config.title
        data["favicon"] = config.favicon
        data["logo"] = config.logo
        data["tagline"] = config.tagline
        data["gdplayer_auth"] = config.gdplayer_auth
        data["custom_header"] = config.custom_header
        data["custom_footer"] = config.custom_footer
        data["description"] = config.description
        data["site_key"] = config.recaptcha_site_key
        data["app_url"] = config.app_url
    most_popular_tv_shows = tvsViewin(1,15)#tv viewed in 1 days
    most_popular_movies = moviesViewin(1,15)#movie viewed in 1 days
    most_popular_shows = list(chain(most_popular_tv_shows,most_popular_movies))
    most_popular_shows_sorted = sorted(most_popular_shows,key=lambda a:a["views"],reverse=True)
    data["pages"] = Page.objects.values("title","slug")
    data["most_popular_shows"] = most_popular_shows_sorted[:15]
    data["sliders"] = most_popular_shows_sorted[:5]
    data["featured"] = TV.objects.filter(published=True,added_on__gte=(datetime.date.today()-datetime.timedelta(days=7))).order_by("-vote_average")[:21]
    data["genres"]=sorted(Genre.objects.all(),key=lambda genre:genre.movie.count()+genre.tv.count(),reverse=True)[:15]
    return data
KEYS = ['title', 'favicon', 'logo', 'tagline', 'custom_header','gdplayer_auth','custom_footer', 'description', 'site_key', 'app_url', 'pages', 'most_popular_shows', 'sliders', 'featured', 'genres']
def config(request=None): 
    data = cache.get_many(KEYS)
    if not data:
        data = cache_context()
        cache.set_many(data,settings.CACHE_TIME)
    return data