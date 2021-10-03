from django.shortcuts import render
from django.views.generic import TemplateView
class HomeView(TemplateView):
    template_name = "webapp/index.html"
class DetailView(TemplateView):
    template_name = "webapp/detail.html"