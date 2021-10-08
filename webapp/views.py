from django.shortcuts import render
from itertools import chain
from .models import Configuration, Movie, TV
from django.views.generic import DetailView, TemplateView
from datetime import date


class HomeView(TemplateView):
    template_name = "webapp/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        config = Configuration.objects.filter(id=1)
        if config.exists():
            config = config.first()
            context["title"] = config.title
            context["favicon"] = config.favicon
            context["logo"] = config.logo
            context["tagline"] = config.tagline
            context["description"] = config.description
            context["custom_header"] = config.custom_header
            context["custom_footer"] = config.custom_footer
        popular_this_month = list(chain(Movie.objects.filter(published=True).order_by(
            "-views")[:10], TV.objects.filter(published=True).order_by("-views")[:10]))
        popular_this_month = sorted(
            popular_this_month, key=lambda show: show.views, reverse=True)
        context["popular_this_month"] = popular_this_month
        context["latest_movies"] = Movie.objects.filter(published=True)[:20]
        context["latest_dramas"] = TV.objects.filter(published=True)[:20]
        upcoming = list(chain(
            Movie.objects.filter(published=True, release_date__gt=date.today()).order_by(
                "release_date")[:10],
            TV.objects.filter(published=True, release_date__gt=date.today()).order_by(
                "release_date")[:10]
        )
        )
        context["upcoming"] = sorted(upcoming,key=lambda show:(show.release_date-date.today()).total_seconds())
        return context
class MovieDetailView(DetailView):
    model = Movie
    template_name = "webapp/details.html"
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        config = Configuration.objects.filter(id=1)
        object = self.object
        if config.exists():
            config = config.first()
            context["title"] = config.title
            context["favicon"] = config.favicon
            context["logo"] = config.logo
            context["tagline"] = config.tagline
            context["custom_header"] = config.custom_header
            context["custom_footer"] = config.custom_footer
        context["description"] = object.overview
        context["images"] = [object.poster_path,object.backdrop_path]
        return context