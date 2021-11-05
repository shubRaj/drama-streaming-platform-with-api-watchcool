from webapp.models import ViewLog, Genre, WatchEpisode, Movie, TV,WatchMovie
import datetime
from . import serializers
from urllib.parse import urlparse
from itertools import chain
from django.core.paginator import Paginator,EmptyPage
from webapp.context_processors import moviesViewin, tvsViewin
from django.db.models import Q
def replaceSingle(single):
    single["tmdb_id"] = str(single.pop("themoviedb_id"))
    single["imdb_external_id"] = single.pop("imdb_id")
    if single["trailer"]:
        single["preview_path"] = single["trailer"].split(("/"))[-1]
        single.pop('trailer')
    single["active"] = 1 if single.pop("published") else 0
    single["runtime"] = single["runtime"]
    single[
        "backdrop_path"] = f'http://image.tmdb.org/t/p/w500/{single["backdrop_path"].split("/")[-1]}'
    single[
        "poster_path"] = f'http://image.tmdb.org/t/p/w500/{single["poster_path"].split("/")[-1]}'
    single["original_name"] = single.pop("original_title")
    single["views"] = ViewLog.objects.filter(tv=single["id"]).count(
    ) if single["media_type"] == "TV" else ViewLog.objects.filter(movie=single["id"]).count()
    single["featured"] = 0
    single["premium"] = 0
    single["pinned"] = 0
    single["created_at"] = single.pop("added_on")
    single["updated_at"] = single.pop("updated_on")
    single["hd"] = 0
    genreslist = Genre.objects.filter(
        movie=single["id"]) if single["media_type"] == "MOVIE" else Genre.objects.filter(tv=single["id"])
    single["genreslist"] = [
        data["name"] for data in serializers.GenreSerializer(genreslist, many=True,).data
    ]
    if single["media_type"] == "MOVIE":
        single["type"] = "movie"
        single["substitle"] = 0
        single["substype"] = 0
        single["videos"] = []
        single["skiprecap_start_in"] = 0
        single["hasrecap"] = 0
        single["substitles"] = []
    else:
        single["name"] = single.pop("title")
        single["type"] = "serie"
        single["first_air_date"] = single.pop("release_date")
        single["hasubs"] = 0
        single["newEpisodes"] = 0
    single["genres"] = [{"name": genre} for genre in single["genreslist"]]
    return single


def replaceMeta(data):
    if isinstance(data, list):
        for single in data:
            replaceSingle(single)
    else:
        replaceSingle(data)
    return data
def singleMovie(resp_data):
    resp_data = replaceMeta(resp_data)
    resp_data["videos"] = []
    watchmovie_serializer = serializers.WatchMovieSerializer(
        WatchMovie.objects.filter(Q(source="XStreamCDN")|Q(url__icontains="streaming.php"), movie=resp_data["id"],), many=True)
    if watchmovie_serializer.data:
        for watchmovie in watchmovie_serializer.data:
            resp_data["videos"].append(watchmovie)
            watchmovie["movie_id"] = watchmovie.pop("movie")
            watchmovie["server"] = watchmovie.pop("source")
            if watchmovie["server"] == "XStreamCDN":
                watchmovie["link"] = f'https://fembed.com{urlparse(watchmovie.pop("url")).path}'
                watchmovie["lang"] = watchmovie.pop("language")
                watchmovie["supported_hosts"] = 1
                watchmovie["hls"] = 0
            else:
                watchmovie["server"] = "Watch Only Server"
                watchmovie["link"] = f'https://asian.watchcool.in/watch/?source={watchmovie.pop("url")}'
                watchmovie["lang"] = watchmovie.pop("language")
                watchmovie["supported_hosts"] = 0
                watchmovie["hls"] = 1
            watchmovie["embed"] = 0
            watchmovie["youtubelink"] = 0
            watchmovie['status'] = "1"
            watchmovie["created_at"] = watchmovie.pop("added_on")
            watchmovie["updated_at"] = watchmovie.pop("created_at")
    return resp_data
def singleEpisode(episode:dict,backdrop_path="http://image.tmdb.org/t/p/w500/None"):
    episode["season_id"] = episode.pop("season")
    episode["tmdb_id"] = episode.pop("tmdb_episode_id")
    episode["still_path"] = f"http://image.tmdb.org/t/p/w500/{episode['still_path'].split('/')[-1]}" \
        if not episode["still_path"].endswith("None") else backdrop_path
    episode["updated_at"] = episode["created_at"] = episode["added_on"]
    episode["episode_number"] = episode["episode_number"]
    episode["hasrecap"] = 0
    episode["skiprecap_start_in"] = 0
    episode["videos"] = []
    episode["substitles"] = []
    watchepisode_serializer = serializers.WatchEpisodeSerializer(
        WatchEpisode.objects.filter(source="XStreamCDN", episode=episode["id"],),
        many=True)
    if watchepisode_serializer.data:
        for watchepisode in watchepisode_serializer.data:
            episode["videos"].append(watchepisode)
            watchepisode["episode_id"] = watchepisode.pop(
                "episode")
            watchepisode["server"] = watchepisode.pop("source")
            # if watchepisode["server"]=="XStreamCDN":
            watchepisode["link"] = f'https://fembed.com{urlparse(watchepisode.pop("url")).path}'
            watchepisode["lang"] = watchepisode.pop("language")
            watchepisode["supported_hosts"] = 1
            watchepisode["hls"] = 0
            # else:
            #     watchepisode["link"] = f'https://asian.watchcool.in/watch/?source={watchepisode.pop("url")}'
            #     watchepisode["lang"] = watchepisode.pop("language")
            #     watchepisode["supported_hosts"] = 0
            #     watchepisode["hls"] = 1
            
            watchepisode["embed"] = 0
            watchepisode["youtubelink"] = 0
            watchepisode['status'] = "0"
            watchepisode["created_at"] = watchepisode.pop("added_on")
            watchepisode["updated_at"] = watchepisode["created_at"]
    return episode
def getEpisodes(episode_serializer,backdrop_path="http://image.tmdb.org/t/p/w500/None"):
    episodes = []
    for episode in episode_serializer.data:
        episodes.append(singleEpisode(episode,backdrop_path))
       
    return episodes


def topMovie(number,days=None):
    if days:
        top = Movie.objects.filter(~Q(poster_path__endswith="None"),published=True,release_date__gte=datetime.datetime.now(
        )-datetime.timedelta(days=120)).order_by("-vote_average")[:number]
    else:
        top = Movie.objects.filter(~Q(poster_path__endswith="None"),published=True).order_by("-vote_average")[:number]
    resp_data = replaceMeta(serializers.MovieSerializer(top, many=True).data)
    return resp_data


def topTV(number,days=None):
    if days:
        top = TV.objects.filter(~Q(poster_path__endswith="None"),published=True, updated_on__gte=datetime.datetime.now(
        )-datetime.timedelta(days=120)).order_by("-vote_average")[:number]
    else:
        top = TV.objects.filter(~Q(poster_path__endswith="None"),published=True).order_by("-vote_average")[:number]
    resp_data = replaceMeta(serializers.MovieSerializer(top, many=True).data)
    return resp_data
def latestMovie(number,this_week=False):
    if not this_week:
        latest_releases = Movie.objects.filter(~Q(poster_path__endswith="None"),published=True).order_by("-release_date")[:number]
    else:
        latest_releases = Movie.objects.filter(~Q(poster_path__endswith="None"),published=True,release_date__gte=(datetime.datetime.now()-datetime.timedelta(days=7))).order_by("-release_date")[:number]
    movie_serializer = serializers.MovieSerializer(
    latest_releases, many=True)
    resp_data = replaceMeta(movie_serializer.data)
    return resp_data
def latestTV(number,this_week=False):
    if not this_week:
        latest_releases = TV.objects.filter(~Q(poster_path__endswith="None"),published=True).order_by("-release_date")[:number]
    else:
        latest_releases = TV.objects.filter(~Q(poster_path__endswith="None"),published=True,release_date__gte=(datetime.datetime.now()-datetime.timedelta(days=7))).order_by("-release_date")[:number]
    movie_serializer = serializers.MovieSerializer(
    latest_releases, many=True)
    resp_data = replaceMeta(movie_serializer.data)
    return resp_data
def popularTV(number,days=60):
    popular_series = sorted(tvsViewin(days=days, get=number), key=lambda a: a["views"], reverse=True)
    for popular_serie in popular_series:
        popular_serie["id"] = popular_serie.pop("tv")
    popular_series_serializer = serializers.MovieSerializer(
        popular_series, many=True)
    resp_data = replaceMeta(popular_series_serializer.data)
    return resp_data
def popularMovie(number,days=60):
    popular_series = sorted(moviesViewin(days=days, get=number), key=lambda a: a["views"], reverse=True)
    for popular_serie in popular_series:
        popular_serie["id"] = popular_serie.pop("movie")
    popular_series_serializer = serializers.MovieSerializer(
        popular_series, many=True)
    resp_data = replaceMeta(popular_series_serializer.data)
    return resp_data
def paginate(request,data, per_page=12):
    current_page = request.GET.get("page", "1")
    current_page = int(current_page if current_page.isnumeric() else "1")
    p = Paginator(data, per_page)
    parsed_uri = urlparse(request.build_absolute_uri())
    path = f"{parsed_uri.scheme}://{parsed_uri.netloc}{parsed_uri.path}"
    last_page = p.num_pages
    try:
        page = p.page(current_page)
        has_previous = page.has_previous()
        has_next = page.has_next()
        resp_data = {
            "current_page": current_page,
            "data": page.object_list,
            "first_page_url": f"{path}?page=1",
            "from": 1,
            "last_page": last_page,
            "last_page_url": f"{path}?page={last_page}",
            "links": [
                    {
                        "url": f"{path}?page={page.previous_page_number()}" if has_previous else None,
                        "label": "&laquo; Previous",
                        "active": (page.previous_page_number() == current_page) if has_previous else False
                    }
            ]+[
                {
                    "url": f"{path}?page={link}",
                    "label": link,
                    "active": current_page == link
                } for link in range(1, last_page+1)
            ]+[
                {
                    "url": f"{path}?page={page.next_page_number()}" if has_next else None,
                    "label": "Next &raquo;",
                    "active": (current_page == page.next_page_number()) if has_next else False
                }
            ],
            "prev_page_url": f"{path}?page={page.previous_page_number()}" if has_previous else None,
            "next_page_url": f"{path}?page={page.next_page_number()}" if has_next else None,
            "path": path,
            "per_page": per_page,
            "to": None,
            "total": p.count,
        }
    except EmptyPage:
        resp_data = {
            "current_page": current_page,
            "data": [],
            "first_page_url": f"{path}?page=1",
            "from": 1,
            "last_page": last_page,
            "last_page_url": f"{path}?page={last_page}",
            "links": [
                {
                    "url": f"{path}?page={link}",
                    "label": link,
                    "active": current_page == link
                } for link in range(1, last_page+1)
            ],
            "prev_page_url": None,
            "next_page_url": None,
            "path": path,
            "per_page": per_page,
            "to": None,
            "total": p.count,
        }
    return resp_data