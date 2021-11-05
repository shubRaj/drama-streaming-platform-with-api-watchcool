from django.urls import path
from .import views
app_name = "app_adminDashboard"
urlpatterns = [
    path("movies/",views.MoviesView.as_view(),name="movies"),
    path("tvs/",views.TVsView.as_view(),name="tvs"),
    path("reviews/",views.ReviewView.as_view(),name="reviews"),
    path("users/",views.UsersView.as_view(),name="users"),
    path("import/tv/",views.ImportTVView.as_view(),name="import_tv"),
    path("import/movie/",views.ImportMovieView.as_view(),name="import_movie"),
    path("import/remote/",views.RemoteImport.as_view(),name="import_remote"),
    path("import/",views.ImportView.as_view(),name="import"),
    path("search/",views.SearchView.as_view(),name="search"),
    path("delete/movie/<int:pk>/",views.DeleteMovieView.as_view(),name="delete_movie"),
    path("delete/tv/<int:pk>/",views.DeleteTVView.as_view(),name="delete_tv"),
    path("delete/review/<int:pk>/",views.DeleteReviewView.as_view(),name="delete_review"),
    path("delete/user/<int:pk>/",views.DeleteUserView.as_view(),name="delete_user"),
    path("",views.HomeView.as_view(),name="home"),
]
