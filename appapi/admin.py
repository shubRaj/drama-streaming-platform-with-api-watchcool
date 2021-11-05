from django.contrib import admin
from .models import Configuration
class DisplayConfiguration(admin.ModelAdmin):
    list_display = ("app_name","latestVersion","streaming","anime",)
admin.site.register(Configuration,DisplayConfiguration)