from django.urls import path
from . import views
app_name = "app_webapp"
urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("movie/<int:pk>/", views.MovieDetailView.as_view(), name="movie_detail")
]