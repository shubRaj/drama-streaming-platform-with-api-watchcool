from .urls import urlpatterns
from django.urls import path,include
urlpatterns.extend(
    [
        path("",include("appapi.urls",namespace="appapi")), 
    ]
)