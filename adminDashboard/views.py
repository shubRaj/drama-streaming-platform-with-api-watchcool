from urllib import parse
from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from webapp.models import Movie, TV, ViewLog, Review,Configuration,Genre,Cast,Status,Season,Episode,WatchEpisode,WatchMovie,DownloadMovie,DownloadEpisode
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404
from itertools import chain
from django.http import JsonResponse
import string
import asyncio
from .dramaScraper import Drama
from urllib.parse import urlparse
from django.db.models import Q
import datetime,requests
from django.core.cache import cache
from .utils import get_realtime_user
from .gdplayer import GDPlayer
USER = get_user_model()
csrf_protected_method = method_decorator(csrf_protect)


class DashboardBaseView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name__icontains='manager').exists()

    def handle_no_permission(self):
        raise Http404
def title_to_tmdb(title):
    base_url = "https://api.themoviedb.org/3/search/multi?api_key={api_key}&language=en-US&query={query}&include_adult=true"
    config = Configuration.objects.filter(id=1)
    results = []
    if config.exists():
        themoviedb_api_key = config.first().themoviedb_api_key
        results = requests.get(base_url.format(api_key=themoviedb_api_key,query=title)).json()["results"]
        results = sorted([{
            "poster_path":f"https://www.themoviedb.org/t/p/original{result['poster_path']}",
            "id":result["id"],
            "media_type":result["media_type"],
            "title":result.get("title") or result.get("name"),
            "overview":result["overview"],
            "release_date":result.get("release_date") or result.get("first_air_date"),
            "original_language":result.get("original_language"),
            "popularity":result.get("popularity",0),
        } for result in results if result.get("media_type","").lower() == "movie" or result.get("media_type","").lower() == "tv"],key=lambda a:a.get("popularity"),reverse=True)
    return results
def importMovie(request,id):
    base_url = "https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US&append_to_response=external_ids"
    movie_videos_url = "https://api.themoviedb.org/3/movie/{id}/videos?api_key={api_key}&language=en-US"
    credits_url = "https://api.themoviedb.org/3/movie/{id}/credits?api_key={api_key}&language=en-US"
    poster_base_url = "https://image.tmdb.org/t/p/w220_and_h330_face"
    backdrop_base_url = "https://image.tmdb.org/t/p/w1920_and_h800_multi_faces"
    watchasian_search = "https://was.watchcool.in/search/?q={title}"
    watchasian_episodes = "https://was.watchcool.in/episodes/?url={url}"
    watchasian_links = "https://was.watchcool.in/?url={url}"
    movie_show = Movie.objects.filter(themoviedb_id=int(id))

    if not movie_show.exists():
        config = Configuration.objects.filter(id=1)
        if config.exists():
            api_key = config.first().themoviedb_api_key
            base_resp = requests.get(base_url.format(id=id,api_key=api_key))
            if base_resp.status_code == 200:
                base_data = base_resp.json()
                trailer = ""
                movie_videos_resp = requests.get(movie_videos_url.format(id=id,api_key=api_key))
                if movie_videos_resp.status_code == 200:
                    movie_videos_resp = movie_videos_resp.json()
                    for video in movie_videos_resp["results"]:
                        if (video["site"].lower() == "youtube") and (video["type"].lower() == "trailer"):
                            trailer = f"https://www.youtube.com/embed/{video['key']}"
                            break
                movie_show = Movie.objects.create(
                    themoviedb_id = base_data["id"],
                    imdb_id = base_data["external_ids"].get("imdb_id"),
                    original_title = base_data["original_title"],
                    title = base_data["title"],
                    overview = base_data["overview"],
                    backdrop_path = f"{backdrop_base_url}{base_data['backdrop_path']}",
                    poster_path = f"{poster_base_url}{base_data['poster_path']}",
                    release_date = base_data["release_date"],
                    tagline = base_data["tagline"],
                    runtime = base_data["runtime"],
                    vote_average=base_data["vote_average"],
                    trailer=trailer,
                )
                title = base_data["title"]
                for char in f"{string.punctuation}·":
                    if char in title:
                        title = title.replace(char," ")
                watchasian_url = requests.get(watchasian_search.format(title = f"{title}")).json().get("url")
                if watchasian_url:
                    watchasian_episodes = requests.get(watchasian_episodes.format(url=watchasian_url)).json()["sources"]
                    gdplayer_auth = cache.get("gdplayer_auth",None)
                    if not gdplayer_auth:
                        messages.info(request,"GDPlayer authentication is not configured",fail_silently=True)
                    for episode in watchasian_episodes:
                        watchasian_sources = requests.get(watchasian_links.format(url=episode)).json()["sources"]
                        gdplayer_added=False
                        for movie_link in watchasian_sources:
                            source = urlparse(movie_link).netloc
                            WatchMovie.objects.create(
                                movie=movie_show,
                                source= "XStreamCDN" if source in ("fplayer.info","embedsito.com","diasfem.com","fembed.com") else source,
                                url=movie_link)
                            if gdplayer_auth and not gdplayer_added:
                                try:
                                    if source in ("fplayer.info","embedsito.com","diasfem.com","fembed.com",
                                    "mixdrop.to","streamtape.com","mp4upload.com",):
                                        key = GDPlayer().get_slug(url=movie_link,auth=gdplayer_auth)
                                        if key:
                                            DownloadMovie.objects.create(
                                                movie=movie_show,
                                                original_url=movie_link,
                                                source=source,
                                                slug=key,
                                            )
                                            gdplayer_added=True
                                        else:
                                            messages.error(request,f"Unable to add download link because GDPlayer is not responding",fail_silently=True)
                                except Exception as e:
                                    messages.error(request,"Error while adding download link",fail_silently=True)
                else:
                    messages.error(request,f"Cannot find {base_data['title']} on watchasian",fail_silently=True)
                for genre in base_data["genres"]:
                    genre_obj = Genre.objects.filter(name=genre["name"])
                    if genre_obj.exists():
                        genre_obj.first().movie.add(movie_show)
                    else:
                        Genre.objects.create(name=genre["name"]).movie.add(movie_show)
                casts_resp = requests.get(credits_url.format(id=id,api_key=api_key))
                if casts_resp.status_code == 200:
                    casts_data = casts_resp.json()
                    for cast in casts_data.get("cast"):
                        cast_obj = Cast.objects.filter(name__iexact=cast["name"])
                        if cast_obj.exists():
                            cast_obj.first().movie.add(movie_show)
                        else:
                            Cast.objects.create(
                                name=cast["name"],
                                gender=str(cast["gender"]),
                                tmdb_cast_id=cast["id"],
                                profile_path=f"{poster_base_url}{cast['profile_path']}",
                                popularity=cast.get("popularity",0.00),
                            ).movie.add(movie_show)
                messages.success(request,f"{movie_show.title} added successfully",fail_silently=True)
            else:
                messages.error(request,f"Unable to add Movie",fail_silently=True)
        else:
            messages.error(request,f"TMDB API KEY is missing",fail_silently=True)
    else:
        messages.info(request,f"{movie_show.first().title} already exists in db database.",fail_silently=True)
def importTV(request,id):
    base_url = "https://api.themoviedb.org/3/tv/{id}?api_key={api_key}&language=en-US&append_to_response=external_ids"
    tv_videos_url = "https://api.themoviedb.org/3/tv/{id}/videos?api_key={api_key}&language=en-US"
    episodes_url = "https://api.themoviedb.org/3/tv/{id}/season/{season_number}?api_key={api_key}&language=en-US"
    credits_url = "https://api.themoviedb.org/3/tv/{id}/credits?api_key={api_key}&language=en-US"
    poster_base_url = "https://image.tmdb.org/t/p/w220_and_h330_face"
    backdrop_base_url = "https://image.tmdb.org/t/p/w1920_and_h800_multi_faces"
    watchasian_search = "https://was.watchcool.in/search/?q={title}"
    watchasian_episodes_url = "https://was.watchcool.in/episodes/?url={url}"
    watchasian_links_url = "https://was.watchcool.in/?url={url}"
    tv_show = TV.objects.filter(themoviedb_id=int(id))
    if not tv_show.exists():
        config = Configuration.objects.filter(id=1)
        if config.exists():
            api_key = config.first().themoviedb_api_key
            base_resp = requests.get(base_url.format(id=id,api_key=api_key))
            if base_resp.status_code == 200:
                base_data = base_resp.json()
                trailer_url = ""
                for trailer in requests.get(tv_videos_url.format(id=base_data["id"],api_key=api_key)).json()["results"]:
                    if trailer.get("site").lower()=="youtube" and trailer.get("type").lower()=="trailer":
                        trailer_url = f'https://www.youtube.com/embed/{trailer.get("key")}'
                        break;
                tv_show = TV.objects.create(
                    backdrop_path=f"{backdrop_base_url}{base_data['backdrop_path']}",
                    themoviedb_id=base_data["id"],
                    imdb_id=base_data["external_ids"].get("imdb_id"),
                    original_title=base_data["original_name"],
                    overview=base_data["overview"],
                    poster_path=f"{poster_base_url}{base_data['poster_path']}",
                    release_date=base_data["first_air_date"],
                    title=base_data["name"],
                    trailer=trailer_url,
                    tagline=base_data["tagline"],
                    vote_average=base_data["vote_average"],
                    runtime=base_data["episode_run_time"][0] if base_data["episode_run_time"] else 0
                    )
                seasons = base_data["seasons"]
                title = base_data["name"]
                gdplayer_auth = cache.get("gdplayer_auth",None)
                if not gdplayer_auth:
                    messages.info(request,"GDPlayer authentication is not configured",fail_silently=True)
                for char in f"{string.punctuation}·":
                    if char in title:
                        title = title.replace(char," ")
                if seasons:
                    for season in seasons:
                        if season["season_number"] != 0:
                            season_obj = Season.objects.create(
                                tv=tv_show,
                                tmdb_season_id=season['id'],
                                season_number=season["season_number"],
                                name=season["name"],
                                episode_count=season["episode_count"],
                                overview=season["overview"],
                                poster_path=f"{poster_base_url}{season['poster_path']}",
                                air_date=season["air_date"]
                            )
                            episodes_resp = requests.get(episodes_url.format(id=id,season_number=season["season_number"],api_key=api_key))
                            if episodes_resp.status_code == 200:
                                episodes_data = episodes_resp.json()
                                episodes = episodes_data["episodes"]
                                watchasian_url = requests.get(watchasian_search.format(
                                    title = f"{title} {'season '+str(season['season_number']) if not season['season_number']==1 else ''} ")
                                    ).json().get("url")
                                if watchasian_url:
                                    watchasian_episodes = requests.get(watchasian_episodes_url.format(
                                        url=watchasian_url
                                    )).json()["sources"]
                                    for episode,watchasian_episode in list(zip(episodes,watchasian_episodes)):
                                        episode_obj = Episode.objects.create(
                                            season = season_obj,
                                            name = episode["name"],
                                            overview = episode["overview"],
                                            episode_number = episode["episode_number"],
                                            season_number = episode["season_number"],
                                            tmdb_episode_id = episode["id"],
                                            still_path = f'{poster_base_url}{episode["still_path"]}',
                                            vote_average = episode["vote_average"],
                                            air_date = episode["air_date"] if episode["air_date"] else None
                                        )
                                        watchasian_episode_links = requests.get(watchasian_links_url.format(url=watchasian_episode)).json()["sources"]
                                        gdplayer_added=False
                                        for watchasian_episode_link in watchasian_episode_links:
                                            source = urlparse(watchasian_episode_link).netloc
                                            WatchEpisode.objects.create(
                                                source = "XStreamCDN" if source in ("fplayer.info","embedsito.com","diasfem.com","fembed.com") else source,
                                                episode = episode_obj,
                                                url = watchasian_episode_link
                                            )
                                            if gdplayer_auth and not gdplayer_added:
                                                try:
                                                    if source in ("fplayer.info","embedsito.com","diasfem.com","fembed.com",
                                                    "mixdrop.to","streamtape.com","mp4upload.com",):
                                                        key = GDPlayer().get_slug(url=watchasian_episode_link,auth=gdplayer_auth)
                                                        if key:
                                                            DownloadEpisode.objects.create(
                                                                episode=episode_obj,
                                                                original_url=watchasian_episode,
                                                                source=source,
                                                                slug=key,
                                                            )
                                                            gdplayer_added=True
                                                        else:
                                                            messages.error(request,f"Unable to add download link because GDPlayer is not responding",fail_silently=True)
                                                except Exception as e:
                                                    messages.error(request,"Error while adding download link",fail_silently=True)
                                else:
                                    messages.error(request,f"Cannot find {base_data['name']} {'season '+str(season['season_number']) if season['season_number'] != 1 else ''} on watchasian",fail_silently=True)
                                    break;
                for genre in base_data["genres"]:
                    genre_obj = Genre.objects.filter(name=genre["name"])
                    if genre_obj.exists():
                        genre_obj.first().tv.add(tv_show)
                    else:
                        Genre.objects.create(name=genre["name"]).tv.add(tv_show)
                if base_data["status"]:
                    status_obj = Status.objects.filter(name=base_data["status"])
                    if status_obj.exists():
                        status_obj.first().tv.add(tv_show)
                    else:
                        Status.objects.create(
                            name=base_data["status"]
                        ).tv.add(tv_show)
                casts_resp = requests.get(credits_url.format(id=id,api_key=api_key))
                if casts_resp.status_code == 200:
                    casts_data = casts_resp.json()
                    for cast in casts_data.get("cast"):
                        cast_obj = Cast.objects.filter(name__iexact=cast["name"])
                        if cast_obj.exists():
                            cast_obj.first().tv.add(tv_show)
                        else:
                            Cast.objects.create(
                                name=cast["name"],
                                gender=str(cast["gender"]),
                                tmdb_cast_id=cast["id"],
                                profile_path=f"{poster_base_url}{cast['profile_path']}",
                                popularity=cast.get("popularity",0.00),
                            ).tv.add(tv_show)
                messages.success(request,f"{tv_show.title} added successfully",fail_silently=True)
            else:
                messages.error(request,f"Unable to add TV Show",fail_silently=True)
        else:
            messages.error(request,f"TMDB API KEY is missing",fail_silently=True)
    else:
        messages.info(request,f"{tv_show.first().title} already exists in db database.",fail_silently=True)
class HomeView(DashboardBaseView, View):
    template_name = "adminDashboard/index.html"

    def get(self, request):
        top_rated_shows = list(chain(Movie.objects.order_by(
            "-vote_average")[:5], TV.objects.order_by("-vote_average")[:5]))
        latest_shows = list(
            chain(Movie.objects.all()[:5], TV.objects.all()[:5]))
        new_users = USER.objects.order_by("-date_joined")[:10]
        data = {
            "unique_view": 0,
            "top_rated_shows": sorted(top_rated_shows, key=lambda show: show.vote_average, reverse=True)[:10],
            "latest_shows": sorted(latest_shows, key=lambda show: show.added_on, reverse=True)[:10],
            "new_users": new_users,
            "unique_views_today": ViewLog.objects.filter(viewed_on__date=datetime.date.today()).count(),
            "active_users": get_realtime_user(),
            "shows_published_this_month": (
                Movie.objects.filter(
                    added_on__date__gt=datetime.date.today()-datetime.timedelta(days=30), published=True).count()
            )+(
                TV.objects.filter(added_on__date__gt=datetime.date.today(
                )-datetime.timedelta(days=30), published=True).count()
            ),
            # "draft_shows": (
            #     Movie.objects.filter(published=False).count()
            # )+(
            #     TV.objects.filter(published=False).count()
            # ),
            "new_reviews_today": Review.objects.filter(added_on__date=datetime.date.today()).count(),
            "latest_reviews":Review.objects.filter(approved=True)[:10],
        }
        return render(request, self.template_name, data)


class MoviesView(DashboardBaseView, ListView):
    template_name = "adminDashboard/movies.html"
    paginate_by = 50
    model = Movie
    context_object_name = "movies"

    @csrf_protected_method
    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            id = request.POST.get("id")
            action = request.POST.get("action")
            if id and action:
                if action == "status":
                    ins = self.model.objects.filter(id=id)
                    if ins.exists():
                        if ins.first().published:
                            ins.update(published=False)
                        else:
                            ins.update(published=True)
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["label"] = "Movies"
        return context
class TVsView(MoviesView):
    template_name = "adminDashboard/tvs.html"
    model = TV
    context_object_name = "tvs"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["label"] = "TVs"
        return context
class ReviewView(DashboardBaseView,ListView):
    template_name = "adminDashboard/reviews.html"
    model = Review
    paginate_by = 50
    context_object_name = "reviews"
    @csrf_protected_method
    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            id = request.POST.get("id")
            action = request.POST.get("action")
            if id and action:
                if action == "status":
                    ins = self.model.objects.filter(id=id)
                    if ins.exists():
                        if ins.first().approved:
                            ins.update(approved=False)
                        else:
                            ins.update(approved=True)
        return super().get(request, *args, **kwargs)
class UsersView(DashboardBaseView,ListView):
    template_name = "adminDashboard/users.html"
    model = USER
    paginate_by = 50
    context_object_name = "users"
    def get_queryset(self):
        return self.model.objects.filter(~Q(is_superuser=True))
    @csrf_protected_method
    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            id = request.POST.get("id")
            action = request.POST.get("action")
            if id and action:
                if action == "status":
                    ins = self.model.objects.filter(id=id)
                    if ins.exists():
                        if ins.first().approved:
                            ins.update(approved=False)
                        else:
                            ins.update(approved=True)
        return super().get(request, *args, **kwargs)

class DeleteMovieView(DashboardBaseView, DeleteView):
    model = Movie
    success_url = reverse_lazy("app_adminDashboard:movies")
class DeleteTVView(DashboardBaseView,DeleteView):
    model = TV
    success_url = reverse_lazy("app_adminDashboard:tvs")
class DeleteReviewView(DashboardBaseView, DeleteView):
    model = Review
    success_url = reverse_lazy("app_adminDashboard:reviews")
class DeleteUserView(DashboardBaseView,DeleteView):
    model = USER
    success_url = reverse_lazy("app_adminDashboard:users")
class ImportView(DashboardBaseView,View):
    template_name = "adminDashboard/import.html"
    context_object_name = "shows"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
    
    def post(self,request,*args,**kwargs):
        query = self.request.POST.get("q")
        if query:
            results = title_to_tmdb(query)
            return render(request,self.template_name,{"shows":results,'total':len(results)})
class ImportTVView(DashboardBaseView,View):
    template_name = "adminDashboard/import.html"
    def get(self,request,*args,**kwargs):
        raise Http404
    def post(self,request,*args,**kwargs):
        id = request.POST.get("id")
        if id:
            importTV(request,id)
        return render(request,self.template_name)
class ImportMovieView(DashboardBaseView,View):
    template_name = "adminDashboard/import.html"
    def get(self,request,*args,**kwargs):
        raise Http404
    def post(self,request,*args,**kwargs):
        id = request.POST.get("id")
        if id:
            importMovie(request,id)
        return render(request,self.template_name)

class RemoteImport(DashboardBaseView,View):
    def get(self,request):
        watch_asian_url = request.GET.get("url")
        if watch_asian_url:
            title,season_number,episode_number = asyncio.run(Drama().get_title_from_url(watch_asian_url))
            tmdb_data = title_to_tmdb(title)
            if tmdb_data:
                for tmdb in tmdb_data:
                    if tmdb.get("original_language") in ("ko","zh","ja","th","es"):
                        try:
                            if tmdb.get("media_type")=="movie":
                                importMovie(request,id=tmdb.get("id"))
                            else:
                                importTV(request,id=tmdb.get("id"))
                            return JsonResponse({"status":"Success"})
                        except Exception as e:
                            return JsonResponse({"status":"Server Error","exception":e},status=500)
            else:
                return JsonResponse({"status":"NOT FOUND"},status=404)
        return JsonResponse({"status":"Bad Request"},status=400)
class SearchView(DashboardBaseView,ListView):
    paginate_by = 40
    template_name = "adminDashboard/movies.html"
    def get_queryset(self):
        query = self.request.GET.get("q")
        filter = self.request.GET.get("filter")
        result = []
        if query:
            result = list(chain(Movie.objects.filter(title__icontains=query),TV.objects.filter(title__icontains=query)))
            if filter:
                if filter.lower() == "rating":
                    result = sorted(result,key=lambda show:show.vote_average,reverse=True)
        return result
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["label"] = "Search Results"
        return context