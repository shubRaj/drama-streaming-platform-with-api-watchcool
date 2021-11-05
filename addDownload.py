from webapp.models import DownloadMovie,DownloadEpisode,Movie,Episode
from urllib.parse import urlparse
from adminDashboard.gdplayer import GDPlayer
from django.core.cache import cache
gdplayer_auth=cache.get("gdplayer_auth",None)
def deleteExisting():
    DownloadEpisode.objects.all().delete()
    DownloadMovie.objects.all().delete()
def addDownloadMovie():
    for movie in Movie.objects.all():
        for watch_link in movie.watch.all():
            movie_link = watch_link.url
            source = urlparse(movie_link).netloc
            if gdplayer_auth:
                try:
                    if source in ("fplayer.info","embedsito.com","diasfem.com","fembed.com",):
                        key = GDPlayer().get_slug(url=movie_link,auth=gdplayer_auth)
                        if key:
                            DownloadMovie.objects.create(
                                movie=watch_link.movie,
                                original_url=movie_link,
                                source=source,
                                slug=key,
                            )
                        break;
                except Exception as e:
                    pass
def addDownloadTV():
    for episode in Episode.objects.all():
        gdplayer_added = False
        for watch_link in episode.watch_episode.all():
            watchasian_episode_link = watch_link.url
            source = urlparse(watchasian_episode_link).netloc
            if gdplayer_auth and not gdplayer_added:
                try:
                    if source in ("fplayer.info","embedsito.com","diasfem.com","fembed.com",):
                        key = GDPlayer().get_slug(url=watchasian_episode_link,auth=gdplayer_auth)
                        if key:
                            DownloadEpisode.objects.create(
                                episode=watch_link.episode,
                                original_url=watchasian_episode_link,
                                source=source,
                                slug=key,
                            )
                            gdplayer_added=True
                        break;
                except Exception as e:
                    pass
def addAll():
    deleteExisting()
    addDownloadMovie()
    addDownloadTV()