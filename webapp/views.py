from django.utils.decorators import method_decorator
from django.views.generic import TemplateView,DetailView,View,ListView,CreateView
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from webapp.models.config import Page
from .models import Movie,TV,ViewLog,Episode,WatchEpisode,ViewLog,WatchMovie,Cast,Report,Genre,DownloadMovie,DownloadEpisode,Page
from django.shortcuts import render,redirect
from django.db.models import Q,Count,F
from itertools import chain
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .serializers import TVSerializer
from django.http import Http404,JsonResponse
from rest_framework.response import Response
import datetime
import math

class HomeView(TemplateView):
    template_name = "webapp/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_series"] = TV.objects.filter(~Q(poster_path__endswith="None"),published=True,)[:30]
        context["new_movies"] = Movie.objects.filter(~Q(poster_path__endswith="None"),published=True)[:30]
        context["stories"] = sorted(
            list(
                chain(
                    TV.objects.filter(~Q(poster_path__endswith="None"),published=True,added_on__gte=(datetime.date.today()-datetime.timedelta(days=7))).order_by("-vote_average")[:7],
                    Movie.objects.filter(~Q(poster_path__endswith="None"),published=True,added_on__gte=(datetime.date.today()-datetime.timedelta(days=7))).order_by("-vote_average")[:7],
                )
            ),
            key=lambda a:a.vote_average,
            reverse=True
        )[:7]
        context["new_episodes"] = Episode.objects.filter(~Q(still_path__endswith="None"),season__tv__published=True)[:16]
        context["popular_actors"] =  Cast.objects.filter(~Q(profile_path__endswith="None"),added_on__gte=(datetime.date.today()-datetime.timedelta(days=30)))[:12]
        context["currentPage"] = "home"
        return context
class TVDetailView(DetailView):
    template_name = "webapp/tv_detail.html"
    model = TV
    context_object_name = "tv"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["currentPage"] = "tvs"
        title = f"Watch full episodes of {self.object.title} {'({})'.format(self.object.release_date.year) if self.object.release_date else '' } | {self.request.get_host()}"
        context["title"] = title
        context["description"] = f"{self.request.get_host()}, you can watch full episodes of {self.object.title} {'({})'.format(self.object.release_date.year) if self.object.release_date else '' } online with English Subtitle. Watch korean dramas,japanese dramas,chinese dramas and asian dramas online for free and more free dramas online in high quality, without downloading."
        context["seasons"] = self.object.season.all()
        context["watch_now"] = self.object.season.order_by("season_number").first().episode.order_by("episode_number").first()
        return context
class MovieDetailView(DetailView):
    template_name = "webapp/movie_detail.html"
    model = Movie
    context_object_name = "movie"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        ViewLog.objects.create(movie=self.object,user=self.request.user if self.request.user.is_authenticated else None)
        context["currentPage"] = "movies"
        title = f"Watch {self.object.title} {'({})'.format(self.object.release_date.year) if self.object.release_date else '' } Online With English subtitle in FullHD quality | {self.request.get_host()}"
        context["title"] = title
        context["description"] = f"{self.request.get_host()}, you can watch {self.object.title} {'({})'.format(self.object.release_date.year) if self.object.release_date else '' } with English Subtitle. Watch korean dramas,japanese dramas,chinese dramas and asian dramas online for free and more free dramas online in high quality, without downloading."
        if self.object.genre.exists():
            context["similars"] = Movie.objects.filter(~Q(id=self.object.id),published=True,has_genre__name=self.object.genre.first()).order_by("-release_date")[:6]
        context["download_links"] = self.object.download.all()
        sources = list(self.object.watch.filter(~Q(source__contains="asian")).order_by("-source").values("id","url","source"))
        for index,source in enumerate(sources):
            if "sb" in source.get("source",""):
                sources.append(source)
                sources.pop(index)
        context["sources"] = sources
        return context
class EpisodeDetailView(DetailView):
    template = "webapp/episode_detail.html"
    model = Episode
    context_object_name = "episode"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["currentPage"] = "tvs"
        self.season  = self.object.season
        self.tv  = self.season.tv
        ViewLog.objects.create(tv=self.tv,user=self.request.user if self.request.user.is_authenticated else None)
        context['tv'] = self.tv
        context["season"] = self.season
        title = f"Watch {self.tv.title}{f' Season {self.object.season_number}' if self.object.season_number>1 else ''} Episode {self.object.episode_number} Online With English subtitle in FullHD quality | {self.request.get_host()}"
        context["title"] = title
        context["description"] =  f"{self.request.get_host()}, you can watch {self.tv.title} {'({})'.format(self.tv.release_date.year) if self.tv.release_date else '' } {f' Season {self.object.season_number}' if self.object.season_number>1 else ''} Episode {self.object.episode_number} online with English Subtitle. Watch korean dramas,japanese dramas,chinese dramas and asian dramas online for free and more free dramas online in high quality, without downloading."
        context["download_links"] = self.object.download_episode.all()
        next_episode = self.season.episode.filter(episode_number=(math.floor(float(self.object.episode_number)+1)))
        if not next_episode.exists():
            next_season = self.tv.season.filter(season_number=(math.floor(float(self.season.season_number)+1)))
            if next_season.exists():
                next_episode = next_season.first().episode.order_by("episode_number").first()
            else:
                next_episode = None
        else:
            next_episode = next_episode.first()
        if self.tv.genre.exists():
            context["similars"] = TV.objects.filter(~Q(id=self.tv.id),published=True,has_genre__name=self.tv.genre.first()).order_by("-release_date")[:6]
        context["next_episode"] = next_episode
        sources = list(self.object.watch_episode.filter(~Q(source__contains="asian")).order_by("-source").values("id","url","source"))
        for index,source in enumerate(sources):
            if "sb" in source.get("source",""):
                sources.append(source)
                sources.pop(index)
        context["sources"] = sources
        return context
class TVList(ListView):
    model = TV
    template_name = "webapp/show_list.html"
    context_object_name = 'shows'
    paginate_by = 40
    # def post(self,request):
    #     filter,category,rating,released,sorting=itemgetter("_ACTION","category","rating","released","sorting")(request.POST)
    #     return super().get(request)
    def get_queryset(self):
        return self.model.objects.filter(published=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["currentPage"] = "tvs"
        title = f"List all TV Shows | {self.request.get_host()}"
        context["title"] = title
        context["description"] = title
        return context
class MovieList(TVList):
    model = Movie
    template_name = "webapp/show_list.html"
    context_object_name = 'shows'
    paginate_by = 40
    # def post(self,request):
    #     filter,category,rating,released,sorting=itemgetter("_ACTION","category","rating","released","sorting")(request.POST)
    #     return super().get(request)
    def get_queryset(self):
        return self.model.objects.filter(published=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"List all Movies | {self.request.get_host()}"
        context["title"] = title
        context["description"] = title
        context["currentPage"] = "movies"
        return context
class ActorList(ListView):
    model = Cast
    paginate_by = 40
    template_name = "webapp/actor_list.html"
    context_object_name = "actors"
    def get_queryset(self):
        return self.model.objects.filter(~Q(profile_path__endswith="None")).order_by("-added_on","-popularity")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"List all Actors | {self.request.get_host()}"
        context["title"] = title
        context["description"] = title
        context["currentPage"] = "actors"
        return context
class GenreView(ListView):
    template_name = "webapp/show_list.html"
    context_object_name = "shows"
    paginate_by = 40
    def get_queryset(self):
        self.category = self.kwargs["category"]
        shows = sorted(list(chain(TV.objects.filter(has_genre__name__icontains=self.category),Movie.objects.filter(has_genre__name__icontains=self.category))),key=lambda a:a.release_date,reverse=True)
        return shows
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"{self.category} TV Shows and Movies | {self.request.get_host()}"
        context["title"] = title
        context["description"] = title
        context["currentPage"] = "category"
        context["category"] = self.category
        return context
class DiscussionView(TemplateView):
    template_name = "webapp/discussions.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"Discussions | {self.request.get_host()}"
        context["title"] = title
        context["description"] = title
        return context
class DiscoveryView(ListView):
    template_name = "webapp/show_list.html"
    context_object_name = "shows"
    paginate_by = 40
    def get_queryset(self):
        return sorted(list(chain(TV.objects.order_by("-vote_average"),Movie.objects.order_by("-vote_average"))),key=lambda a:a.vote_average,reverse=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"Discovery Top Rated TV Shows and Movies | {self.request.get_host()}"
        context["title"] = title
        context["description"] = title
        context["currentPage"] = "discovery"
        return context
class TrendView(ListView):
    template_name = "webapp/trends.html"
    context_object_name = "shows"
    # paginate_by = 40
    # def get_queryset(self):
        
    #     most_popular_tv_shows = ViewLog.objects.filter(movie=None,viewed_on__gte=(datetime.date.today()-datetime.timedelta(days=1))).values(
    #         "tv",
    #         slug=F("tv__slug"),
    #         title=F("tv__title"),
    #         poster_path=F("tv__poster_path"),
    #         tagline=F("tv__tagline"),
    #         release_date=F("tv__release_date"),
    #         overview=F("tv__overview"),
    #         vote_average=F("tv__vote_average"),
    #         ).annotate(views=Count("tv")).order_by()
    #     most_popular_movies = ViewLog.objects.filter(tv=None,viewed_on__gte=(datetime.date.today()-datetime.timedelta(days=1))).values(
    #         "movie",
    #         slug=F("movie__slug"),
    #         title=F("movie__title"),
    #         poster_path=F("movie__poster_path"),
    #         tagline=F("movie__tagline"),
    #         release_date=F("movie__release_date"),
    #         overview=F("movie__overview"),
    #         vote_average=F("movie__vote_average"),
    #         ).annotate(views=Count("movie")).order_by()
    #     return sorted(list(chain(most_popular_tv_shows,most_popular_movies)),key=lambda a:a["views"],reverse=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"List all trending TV Shows and Movies | {self.request.get_host()}"
        context["title"] = title
        context["description"] = title
        context["currentPage"] = "trends"
        return context
class AjaxEmbed(View):
    template_name = "webapp/embed.html"
    def post(self,request):
        id = request.POST.get("id")
        type = request.POST.get("type")
        if type:
            if id:
                if id.isnumeric():
                    try:
                        if type=="tv":
                            source = WatchEpisode.objects.get(id=int(id))
                        else:
                            source = WatchMovie.objects.get(id=int(id))
                    except (WatchEpisode.DoesNotExist,WatchMovie.DoesNotExist):
                        pass
                    source_url = source.url
                return render(request,self.template_name,{"source_url":source_url})
        return render(request,self.template_name)

class AjaxSearch(generics.ListAPIView):
    def list(self,request):
        queryset = []
        original_queryset = self.get_queryset()
        for show in original_queryset:
            queryset.append(show["show"])
        serializer = TVSerializer(queryset,many=True)
        for i,show in enumerate(original_queryset):
            serializer.data[i]["type"] = show["type"]
            serializer.data[i]["url"] = reverse(f"app_webapp:{'tv_detail' if show['type']=='TV' else 'movie_detail'}",args=(serializer.data[i]["slug"],))
            del serializer.data[i]["slug"]
        return Response({"data":serializer.data})
    def get_queryset(self):
        query = self.request.GET.get("q")
        results = []
        if query:
            tv_shows = TV.objects.filter(published=True,title__icontains=query)[:10]
            movies = Movie.objects.filter(published=True,title__icontains=query)[:10]
            results = sorted([{"show":show,"type":show.__class__.__name__.upper()} for show in chain(tv_shows,movies)],key=lambda show:show["show"].release_date,reverse=True)
        return results
class ReportView(TemplateView):
    template_name = "webapp/report.html"
class CategoryView(ListView):
    template_name = "webapp/category.html"
    context_object_name = "categories"
    def get_queryset(self):
        return sorted(Genre.objects.all(),key=lambda genre:genre.movie.count()+genre.tv.count(),reverse=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"List all Categories | {self.request.get_host()}"
        context["title"] = title
        context["description"] = title
        return context
class AjaxReport(CreateView):
    model = Report
    fields = ("episode","movie","option","description",)
    def form_valid(self, form):
        self.object=form.save()
        return JsonResponse({"status":"success","text":"Thanks for your feedback","data":None})

class SearchView(TemplateView):
    template_name = "webapp/search.html"
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        
        return super().dispatch(request, *args, **kwargs)
    def get(self,request):
        raise Http404
    
    def post(self,request):
        return super().get(request)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.POST.get("q")
        if query:
            context["query"] = query
            movies = Movie.objects.filter(title__icontains=query)[:30]
            tvs = TV.objects.filter(title__icontains=query)[:30]
            actors = Cast.objects.filter(name__icontains=query)[:30]
            context["movies"] = movies
            context["tvs"] = tvs
            context["actors"] = actors
            context["currentPage"] = "home"
            context["total_results"]  = movies.count()+tvs.count()+actors.count()
        title = f"Search Result for {query} | {self.request.get_host()}"
        context["title"] = title
        context["description"] = title
        return context
class ActorDetail(DetailView):
    model = Cast
    context_object_name="actor"
    template_name = "webapp/actor_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["shows"]  = sorted(list(chain(self.object.movie.all()[:15],self.object.tv.all()[:15])),key=lambda a:a.release_date,reverse=True)
        title = f"Watch all TV Shows and Movie casting {self.object.name} | {self.request.get_host()}"
        context["title"] = title
        context["description"] = title
        context["currentPage"]  = "actors"
        return context
class PageDetailView(DetailView):
    model = Page
    context_object_name = "page"
    template_name = "webapp/page.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = f"{self.object.title} | {self.request.get_host()}"
        context["title"] = title
        context["description"] = title
        return context
class TrailerView(View):
    template_name = "webapp/trailer.html"
    def get(self,request):
        trailer = request.GET.get("trailer")
        return render(request,self.template_name,{"trailer":trailer})
class Logout(LoginRequiredMixin,LogoutView):
    pass
class Login(UserPassesTestMixin,LoginView):
    template_name = "webapp/login.html"
    def test_func(self):
        return not self.request.user.is_authenticated
    def handle_no_permission(self):
        return redirect(reverse("app_webapp:home"))
    def get_success_url(self) -> str:
        if self.request.user.is_superuser or self.request.user.groups.filter(name__icontains='manager').exists():
            return reverse("app_adminDashboard:home")
        return super().get_success_url()