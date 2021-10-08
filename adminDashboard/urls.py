from django.urls import path
from .import views
app_name = "app_adminDashboard"
urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("movies/",views.MoviesView.as_view(),name="movies"),
    path("add/",views.Add.as_view(),name="add"),
    path("addpage/",views.AddPageView.as_view(),name="add_page"),
    path("logout/",views.DashboardLogoutView.as_view(),name="logout"),
    path("delete/movie/<int:pk>/",views.DeleteMovieView.as_view(),name="delete_movie"),
]
