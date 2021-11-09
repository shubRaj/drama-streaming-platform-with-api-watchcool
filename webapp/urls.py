from django.urls import path

from watchcool.settings import CACHE_TIME
from . import views
from django.views.decorators.cache import cache_page
from django.conf import settings
CACHE_TIME = settings.CACHE_TIME
app_name = "app_webapp"
urlpatterns = [
    path("watch/tv/<slug:slug>/",views.TVDetailView.as_view(),name="tv_detail"),
    path("tvs/",cache_page(CACHE_TIME)(views.TVList.as_view()),name="tv_list"),
    path("movies/",cache_page(CACHE_TIME)(views.MovieList.as_view()),name="movie_list"),
    path("actors/",cache_page(CACHE_TIME)(views.ActorList.as_view()),name="actor_list"),
    path("search/",views.SearchView.as_view(),name="search"),
    path("actor/<slug:slug>/",views.ActorDetail.as_view(),name="actor_detail"),
    path("watch/movie/<slug:slug>/",views.MovieDetailView.as_view(),name="movie_detail"),
    path("watch/episode/<slug:slug>/",views.EpisodeDetailView.as_view(),name="watch_episode"),
    path("category/<str:category>/",views.GenreView.as_view(),name="category"),
    path("ajax/embed/",views.AjaxEmbed.as_view(),name="embed"),
    path("ajax/search/",views.AjaxSearch.as_view(),name="ajax_search"),
    path("ajax/report/",views.AjaxReport.as_view(),name="ajax_report"),
    path("modal/report/tv/<int:episode_id>/",views.ReportView.as_view(),name="report_modal_tv"),
    path("modal/report/movie/<int:movie_id>/",views.ReportView.as_view(),name="report_modal_movie"),
    path("trailer/",views.TrailerView.as_view(),name="trailer"),
    path("discovery/",cache_page(CACHE_TIME)(views.DiscoveryView.as_view()),name="discovery"),
    path("trends/",cache_page(CACHE_TIME)(views.TrendView.as_view()),name="trends"),
    path("discussions/",cache_page(CACHE_TIME)(views.DiscussionView.as_view()),name="discussions"),
    path("category/",cache_page(CACHE_TIME)(views.CategoryView.as_view()),name="category"),
    path("page/<slug:slug>/",cache_page(CACHE_TIME)(views.PageDetailView.as_view()),name="page"),
    path("login/",views.Login.as_view(),name="login"),
    path("logout/",views.Logout.as_view(), name="logout"),
    path("",views.HomeView.as_view(),name="home"),
]