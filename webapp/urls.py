from django.urls import path
from . import views
app_name = "app_webapp"
urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    path("detail/",views.DetailView.as_view(),name="detail"),
]