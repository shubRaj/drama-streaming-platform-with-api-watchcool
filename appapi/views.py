from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, GenericAPIView,CreateAPIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from .models import Configuration
from webapp.models import Movie, TV, ViewLog, Season, Episode, WatchEpisode,Report
from django.db.models import Q, F
from itertools import chain
from urllib.parse import urlparse
from . import serializers
import requests
from django.contrib.auth import get_user_model
from webapp.context_processors import moviesViewin, tvsViewin
from .utils import (replaceMeta, getEpisodes, singleEpisode,
topMovie, topTV,paginate,latestTV,latestMovie,popularTV,popularMovie,singleMovie)
from webapp.context_processors import config
import datetime
_BASE_URL = "https://myapp.watchcool.in/public/api"
class ConfigAPIView(RetrieveAPIView):
    queryset = Configuration.objects.all()
    serializer_class = serializers.ConfigSerializer

    def get(self, request, **kwargs):
        self.kwargs["pk"] = 1
        resp = super().get(request)
        resp.data = requests.get(
            f"{_BASE_URL}/params").json()
        # for key in resp.data.keys():
        #     if isinstance(resp.data[key], bool):

        #         if resp.data[key]:
        #             resp.data[key] = 1
        #         else:
        #             resp.data[key] = 0
        return resp


class SearchAPIView(ListAPIView):
    serializer_class = serializers.MovieSerializer
    queryset = Movie.objects.none()

    def get(self, request, **kwargs):
        self.query = self.kwargs["query"]
        query_results = sorted(
            list(
                chain(
                    Movie.objects.filter(title__icontains=self.query)[:5],
                    TV.objects.filter(title__icontains=self.query)[:5]
                )
            ), key=lambda a: a.vote_average, reverse=True
        )
        serializer = serializers.MovieSerializer(query_results, many=True)
        resp_data = {"search": replaceMeta(serializer.data)}
        return Response(resp_data, status=200, content_type="application/json")


class SerieAPIView(RetrieveAPIView):
    queryset = TV.objects.filter(published=True)
    serializer_class = serializers.MovieSerializer

    def get(self, request, **kwargs):
        resp = super().get(request, **kwargs)
        if resp.data:
            ViewLog.objects.create(tv=self.get_object(),user=request.user if request.user.is_authenticated else None)
            resp.data = replaceMeta(resp.data)
            resp.data["seasons"] = []
            season_serializer = serializers.SeasonSerializer(
                Season.objects.filter(tv=resp.data["id"]), many=True)
            if season_serializer.data:
                for season in season_serializer.data:
                    resp.data["seasons"].append(season)
                    season["tmdb_id"] = season.pop("tmdb_season_id")
                    season["serie_id"] = season.pop("tv")
                    season["created_at"] = season.pop("added_on")
                    season["updated_at"] = season.pop("updated_on")
                    episode_serializer = serializers.EpisodeSerializer(
                        Episode.objects.filter(season=season["id"]), many=True)
                    season["episodes"] = getEpisodes(
                        episode_serializer, backdrop_path=resp.data["backdrop_path"])
        return resp


class MovieAPIView(RetrieveAPIView):
    serializer_class = serializers.MovieSerializer
    queryset = Movie.objects.filter(published=True)

    def get(self, request, **kwargs):
        resp = super().get(request, **kwargs)
        if resp.data:
            ViewLog.objects.create(movie=self.get_object(),user=request.user if request.user.is_authenticated else None)
            resp.data = singleMovie(resp.data)
        return resp


class RelatedSerieAPIView(SearchAPIView):
    model = TV

    def get(self, request, **kwargs):
        self.pk = self.kwargs["pk"]
        try:
            self.object = self.model.objects.get(id=self.pk)
            genres = [genre["name"] for genre in serializers.GenreSerializer(
                self.object.genre.all(), many=True).data]

            query_results = self.model.objects.filter(
                ~Q(id=self.pk),~Q(poster_path__endswith="None"), has_genre__name__in=genres).distinct()[:14]
            serializer = serializers.MovieSerializer(query_results, many=True)
            resp_data = {"relateds": replaceMeta(serializer.data)}
            return Response(resp_data, status=200, content_type="application/json")
        except ObjectDoesNotExist:
            return Response({"relateds": []}, status=404, content_type="application/json")


class RelatedMovieAPIView(RelatedSerieAPIView):
    model = Movie


class SuggestedContentAPIView(SearchAPIView):
    def get(self, request, **kwargs):
        most_popular_shows = cache.get("most_popular_shows", [])
        if not most_popular_shows:
            most_popular_shows = config(request).get("most_popular_show",[])
        for most_popular_show in most_popular_shows:
            most_popular_show.pop("slug")
            most_popular_show["id"] = most_popular_show.pop(
                "movie") if most_popular_show.get("movie") else most_popular_show.pop("tv")
        resp_data = replaceMeta(most_popular_shows)
        return Response({"suggested": resp_data})


class AllGenreAPIView(SearchAPIView):
    def get(self, request, **kwargs):
        genres = cache.get("genres")
        genres = [{"id": genre.id, "name": genre.name}
                  for genre in genres] if genres else []
        return Response({"genres": genres})


class RecommendedAPIView(SuggestedContentAPIView):
    def get(self, request, **kwargs):
        resp = super().get(request, **kwargs)
        resp.data["recommended"] = resp.data.pop("suggested")
        return resp


class FeaturedAPIView(SearchAPIView):
    def get(self, request, **kwargs):
        featured_shows = sorted(
            list(
                chain(
                    moviesViewin(7, 10),
                    tvsViewin(7, 10)
                ),
            ), key=lambda a: a["views"], reverse=True)
        for featured_show in featured_shows:
            featured_show.pop("slug")
            featured_show["id"] = featured_show.pop(
                "movie") if featured_show.get("movie") else featured_show.pop("tv")
        resp_data = replaceMeta(featured_shows)
        return Response({"featured": resp_data})


class TOP10APIView(SearchAPIView):
    def get(self, request, **kwargs):
        # top show from last 2 months
        return Response({"top10": topTV(20,120)})


class LatestReleaseAPIView(SearchAPIView):
    def get(self, request, **kwargs):
        return Response({"latest": latestMovie(20)})


class LatestSerieAPIView(SearchAPIView):
    def get(self, request, **kwargs):
        return Response({"recents": latestTV(20)})


class PopularSerieAPIView(SearchAPIView):

    def get(self, request, **kwargs):
        return Response({"popularSeries": popularTV(20)})


class PopularMovieAPIView(PopularSerieAPIView):

    def get(self, request, **kwargs):
        return Response({"popular":popularMovie(20)})


class NewEpisodeAPIView(ListAPIView):
    queryset = Episode.objects.filter(has_watch_episode__source="XStreamCDN").order_by("-added_on").values(
        "id",
        "episode_number",
        "still_path",
        "vote_average",
        "season",
        "season_number",
        episode_name=F("name"),
        season_name=F("season__name"),
        tv_name=F("season__tv__title"),
        tv_id=F("season__tv__id"),
        tv_backdrop_path=F("season__tv__backdrop_path"),
        serieTmdb=F("season__tv__themoviedb_id"),
        )[:20]
    serializer_class = serializers.EpisodeSerializer

    def get(self, request, **kwargs):
        querysets = self.get_queryset()
        episodes = []
        for episode in querysets:
            episodes.append(episode)
            episode['episode_id'] = episode.pop("id") 
            episode['id'] = episode.pop("tv_id") #uses tv id to fetch other episodes
            episode['still_path'] = f'http://image.tmdb.org/t/p/w500/{episode["still_path"].split("/")[-1] if not episode["still_path"].endswith("None") else episode["tv_backdrop_path"].split("/")[-1]}'
            episode['season_id'] = episode.pop("season")
            episode["name"] = episode.pop("tv_name")
            watch_links = WatchEpisode.objects.filter(episode=episode["episode_id"],url__icontains="streaming.php").values("url","source","language")
            if watch_links.exists():
                watch_link = watch_links.first()
                episode['link'] = f'https://asian.watchcool.in/watch/?source={watch_link["url"]}'
                episode['server'] = "Watch Only Server"
                episode['lang'] = watch_link["language"]
            else:
                episode['link'] = ''
                episode['server'] = ''
                episode['lang'] = ''
            episode['embed'] = '0'
            episode['youtubelink'] = '0'
            episode['hls'] = '1'
            episode['seasons_name'] = episode.pop("season_name")
            episode['premuim'] = 0 
            episode['poster_path']= episode["still_path"]
            episode['hasrecap'] = '0'
            episode['skiprecap_start_in'] = '0'
            episode['supported_hosts'] = '0'
            episode['hd'] = 0
            episode['genreslist'] = []
            episode['hasubs'] = 0
            episode["genres"] = []
        return Response({"latest_episodes":episodes})


class LatestAnimeAPIView(ListAPIView):
    queryset = TV.objects.none()
    serializer_class = serializers.MovieSerializer

    def get(self, request, **kwargs):
        resp = super().get(request, **kwargs)
        resp.data = {"anime": []}
        return resp


class GenreTop10APIView(APIView):
    def get(self, request, **kwargs):
        resp_data = paginate(request,data=topMovie(36,120))
        return Response(resp_data)
class GenreNewAPIView(APIView):
    def get(self,request,**kwargs):
        resp_data = paginate(request,data=latestMovie(36))
        return Response(resp_data)
class GenrePopularMovieAPIView(APIView):
    def get(self,request,**kwargs):
        resp_data = paginate(request,data=popularMovie(36))
        return Response(resp_data)
class NewThisWeekAPIView(APIView):
    def get(self,request,**kwargs):
        new_this_week =  sorted(
            list(
                chain(
                    latestTV(10,this_week=True),latestMovie(10,this_week=True)
                    )
                ),
            key=lambda a:(a.get("release_date") or a.get("first_air_date")),
            reverse=True)
        return Response({"thisweek":new_this_week})
class NewThisWeekGenreAPIView(APIView):
    def get(self,request,**kwargs):
        resp_data = paginate(request,latestMovie(36,this_week=True))
        return Response(resp_data)
class EpisodeShowAPIView(RetrieveAPIView):
    queryset = Episode
    serializer_class = serializers.EpisodeSerializer
    def get(self,request,**kwargs):
        resp = super().get(request,**kwargs)
        resp.data = {"episodes":[singleEpisode(resp.data),]}
        return resp
class MoviesAPIView(APIView):
    model = Movie
    def get(self,request,**kwargs):
        serializer = serializers.MovieSerializer(self.model.objects.filter(published=True).order_by("-release_date")[:60],many=True)
        resp_data = replaceMeta(serializer.data)
        return Response(paginate(request,resp_data))
class SeriesAPIView(MoviesAPIView):
    model = TV
class ChoosedAPIView(ListAPIView):
    queryset = TV.objects.filter(~Q(poster_path__endswith="None"),published=True,has_genre__name__iexact="drama").order_by("-updated_on")[:20]
    serializer_class = serializers.MovieSerializer
    def get(self,request,**kwargs):
        resp = super().get(request,**kwargs)
        resp.data = {"choosed":replaceMeta(resp.data)}
        return resp
class ChoosedGenreAPIView(ChoosedAPIView):
    queryset = Movie.objects.filter(~Q(poster_path__endswith="None"),published=True,has_genre__name__iexact="drama").order_by("-updated_on")[:36]
    def get(self,request,**kwargs):
        resp = super().get(request,**kwargs)
        resp.data = paginate(request,resp.data.pop("choosed"))
        return resp
class GenreLatestEpisodeAPIView(NewEpisodeAPIView):
    def get(self,request,**kwargs):
        resp = super().get(request,**kwargs)
        resp.data = paginate(request,resp.data["latest_episodes"])
        return resp
class GenreRecommendedAPIView(ListAPIView):
    queryset = Movie.objects.filter(~Q(poster_path__endswith="None"),published=True,vote_average__gte=7).order_by("-updated_on")[:36]
    serializer_class = serializers.MovieSerializer
    def get(self,request,**kwargs):
        resp = super().get(request,**kwargs)
        resp.data  = paginate(request,resp.data)
        return resp
class GenrePopularSerieAPIView(APIView):
    def get(self,request,**kwargs):
        datas = popularTV(36)
        return Response(paginate(request,datas))
class TrendingThisWeekAPIView(APIView):
    def get(self,request,**kwargs):
        return Response({"trending":popularTV(20,days=7)})
class GenreTrendingAPIView(APIView):
    def get(self,request,**kwargs):
        return Response(paginate(request,popularMovie(36,7)))
class FilterMovieByNonGenreAPIView(APIView):
    model = Movie
    def get(self,request,filter):
        if filter=="byviews":
            resp_data = popularMovie(20) if self.model.__name__ == "Movie" else popularTV(20)
        elif filter=="byyear" or filter=="latestadded":
            resp_data = latestMovie(20) if self.model.__name__ == "Movie" else latestTV(20)
        else:
            #filter=="byrating":
            resp_data = topMovie(20) if self.model.__name__ == "Movie" else topTV(20)
        return Response(paginate(request,resp_data))
class MovieByGenreAPIView(APIView):
    model = Movie
    def get(self,request,genre_id):
        shows = self.model.objects.filter(~Q(poster_path__endswith="None"),published=True,has_genre__id=genre_id).order_by("-release_date")[:36]
        serializer = serializers.MovieSerializer(shows,many=True)
        datas = []
        for data in serializer.data:
            datas.append(singleMovie(data))
        resp_data = paginate(request,datas)
        return Response(resp_data)
class TVByGenreAPIView(MovieByGenreAPIView):
    model = TV
class  FilterTVByNonGenreAPIView(FilterMovieByNonGenreAPIView):
    model = TV
class GenreLatestSerieAPIView(APIView):
    def get(self,request,**kwargs):
        resp_data = paginate(request,latestTV(36))
        return Response(resp_data)
class RegisterAPIView(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    def post(self,request,**kwargs):
        super().post(request,**kwargs)
        return Response(requests.post(f"{_BASE_URL}/register",data=request.POST).json())
class UserAPIView(APIView):
    def get(self,request):
        resp = requests.get(f"{_BASE_URL}/user",headers={"Authorization":request.META.get("HTTP_AUTHORIZATION")})
        try:
            return Response(resp.json())
        except Exception:
            return Response({"status":"400"},status=400)
class UpdateAccountAPIView(APIView):
    def put(self,request):
        return Response(requests.put(f"{_BASE_URL}/account/update",headers={"Authorization":request.META.get("HTTP_AUTHORIZATION")},data=request.data).json())
class LoginAPIView(APIView):
    def post(self,request):
        return Response(requests.post(f"{_BASE_URL}/login",data=request.POST).json())
class UpcomingAPIView(ListAPIView):
    queryset = TV.objects.filter(release_date__gt=datetime.datetime.now())[:20]
    serializer_class = serializers.MovieSerializer
    def get(self,request,**kwargs):
        resp = super().get(request,**kwargs)
        resp.data = {"upcoming":replaceMeta(resp.data)}
        return resp
class IsSubscribedAPIView(APIView):
    def get(self,request):
        return Response(requests.get(f"{_BASE_URL}/account/isSubscribed",headers={"Authorization":request.META.get("HTTP_AUTHORIZATION")},data=request.GET).json())
class SuggestAPIView(APIView):
    def post(self,request):
        title = request.POST.get("title")
        message = request.POST.get("message")
        serializer = serializers.ReportSerializer(data={"description":message})
        if serializer.is_valid():
            inst = serializer.save()
            resp_data = {
                'status': 200, 
                'message': 'created successfully', 
                'body': {
                    'title': serializer.data.get("title"), 
                    'message': serializer.data.get("message"), 
                    'updated_at': datetime.datetime.now(), 
                    'created_at': datetime.datetime.now(), 
                    'id': inst.id
                    }
                }
            return Response(resp_data)
        return Response({"status":400},status=400)