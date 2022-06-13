from .urls import urlpatterns
from django.urls import path,include
urlpatterns.extend(
    [
        path("web/",include("webapp.urls",namespace="webapp")),
        path("",include("appapi.urls",namespace="appapi")), 

    ]
)