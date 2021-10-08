from django.shortcuts import render
from django.views.generic import View, TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from webapp.models import Movie,TV
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from itertools import chain
USER = get_user_model()
csrf_protected_method = method_decorator(csrf_protect)


class DashboardBaseView(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    def handle_no_permission(self):
        return HttpResponseRedirect("/")
class HomeView(DashboardBaseView, View):
    template_name = "adminDashboard/index.html"
    def get(self, request):
        top_rated_shows = list(chain(Movie.objects.order_by("-vote_average")[:5],TV.objects.order_by("-vote_average")[:5]))
        latest_shows = list(chain(Movie.objects.all()[:5],TV.objects.all()[:5]))
        new_users = USER.objects.order_by("-date_joined")[:5]
        data = {
            "unique_view":0,
            "top_rated_shows":sorted(top_rated_shows,key=lambda show:show.vote_average,reverse=True)[:5],
            "latest_shows":sorted(latest_shows,key=lambda show:show.added_on,reverse=True)[:5],
            "new_users":new_users,
        }
        return render(request, self.template_name,data)

class MoviesView(DashboardBaseView,ListView):
    template_name = "adminDashboard/movies.html"
    paginate_by = 1
    model = Movie
    context_object_name = "movies"

    @csrf_protected_method
    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            id = request.POST.get("id")
            action = request.POST.get("action")
            if id and action:
                if action == "status":
                    ins = Movie.objects.filter(id=id)
                    if ins.exists():
                        if ins.first().published:
                            ins.update(published=False)
                        else:
                            ins.update(published=True)
        return super().get(request, *args, **kwargs)
class DeleteMovieView(DashboardBaseView,DeleteView):
    model = Movie
    success_url = reverse_lazy("app_adminDashboard:movies")
class AddPageView(TemplateView):
    template_name = "adminDashboard/addpage.html"


class Add(TemplateView):
    template_name = "adminDashboard/add.html"


class DashboardLogoutView(LogoutView):
    pass