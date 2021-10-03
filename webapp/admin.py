from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.db import models
from django.utils import timesince
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (Movie, WatchMovie, MovieSubtitle, Genre,
                     Status, Cast, TV, Type, WatchEpisode,
                     EpisodeSubtitle, Episode, Season, Report,
                     Page, Configuration)
from django.utils import timesince
CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = (
        "email",
        "username",
    )


class DisplayAbsShow(admin.ModelAdmin):
    list_display = [
        "themoviedb_id",
        "imdb_id",
        "title",
        "vote_average", "added",
    ]
    search_fields = (
        "themoviedb_id",
        "imdb_id",
        "title",
        "original_title",
    )
    list_filter = (
        "vote_average",
        "original_language"
    )
    date_hierarchy = 'release_date'
    list_per_page = 200
    list_max_show_all = 1000

    def added(self, obj):
        return f"{timesince.timesince(obj.added_on)} ago"


class DisplayMovie(DisplayAbsShow):
    pass


class DisplayTV(DisplayAbsShow):
    def __init__(self, *args, **kwargs):
        self.list_display = super().list_display.copy()
        self.list_display.insert(3, "seasons")
        super(DisplayTV, self).__init__(*args, **kwargs)

    def seasons(self, obj):
        return obj.season.count()


class DisplayAbsWatch(admin.ModelAdmin):
    search_fields = [
        "url",
    ]
    list_filter = (
        "source",
        "is_downloadable",
    )
    list_display = [
        "source",
        "url",
        "is_downloadable",
    ]
    list_per_page = 200
    list_max_show_all = 1000


class DisplayAbsSubtitle(admin.ModelAdmin):
    search_fields = ["url", ]
    list_display = ["url", ]
    list_per_page = 200
    list_max_show_all = 1000


class DisplayEpisodeSubtitle(DisplayAbsSubtitle):
    def __init__(self, *args, **kwargs):
        self.search_fields = super().search_fields.copy()
        self.list_display = super().list_display.copy()
        self.search_fields.extend(
            [
                "episode__season__tv__title",
                "episode__name",
                "episode__season__tv__themoviedb_id",
                "episode__season__tv__imdb_id",
                "episode__name",
                "episode__season__name",
            ]
        )
        self.list_display.insert(0, "episode")
        self.list_display.insert(0, "season")
        self.list_display.insert(0, "title")
        super(DisplayEpisodeSubtitle, self).__init__(*args, **kwargs)

    def season(self, obj):
        return obj.episode.season.name

    def title(self, obj):
        return obj.episode.season.tv.title


class DisplayMovieSubtitle(DisplayAbsSubtitle):
    def __init__(self, *args, **kwargs):
        self.search_fields = super().search_fields.copy()
        self.list_display = super().list_display.copy()
        self.search_fields.extend(
            [
                "movie__title",
                "movie__themoviedb_id",
                "movie__imdb_id",
            ]
        )
        self.list_display.insert(0, "movie")
        super(DisplayMovieSubtitle, self).__init__(*args, **kwargs)


class DisplayWatchMovie(DisplayAbsWatch):
    def __init__(self, *args, **kwargs):
        self.list_display = super().list_display.copy()
        self.search_fields = super().search_fields.copy()
        self.search_fields.extend(
            [
                "movie__title",
                "movie__themoviedb_id",
                "movie__imdb_id",
            ]
        )
        self.list_display.insert(0, "movie")
        super(DisplayWatchMovie, self).__init__(*args, **kwargs)


class DisplayWatchEpisode(DisplayAbsWatch):
    def __init__(self, *args, **kwargs):
        self.list_display = super().list_display.copy()
        self.search_fields = super().search_fields.copy()
        self.search_fields.extend(
            [
                "episode__name",
                "episode__season__name",
                "episode__season__tmdb_season_id",
                "episode__season__tv__imdb_id",
                "episode__season__tv__themoviedb_id",
                "episode__season__tv__title",
                "episode__season__name",
            ]
        )
        self.list_display.insert(0, "episode")
        self.list_display.insert(0, "season")
        self.list_display.insert(0, "title")
        super(DisplayWatchEpisode, self).__init__(*args, **kwargs)

    def season(self, obj):
        return obj.episode.season.name

    def title(self, obj):
        return obj.episode.season.tv.title


class DisplayEpisode(admin.ModelAdmin):
    search_fields = [
        "name",
        "tmdb_episode_id",
        "season__name",
        "season__tmdb_season_id",
        "season__tv__themoviedb_id",
        "season__tv__imdb_id",
        "season__tv__title",
        "season__tv__original_title",
    ]
    list_filter = (
        "vote_average",
        "episode_number",
        "season_number",
    )
    list_display = [
        "title",
        "season",
        "name",
        "season_number",
        "episode_number",
        "tmdb_episode_id",
        "vote_average",
    ]
    list_per_page = 200
    list_max_show_all = 1000
    date_hierarchy = "air_date"

    def title(self, obj):
        return obj.season.tv.title


class DisplaySeason(admin.ModelAdmin):
    search_fields = (
        "tmdb_season_id",
        "name",
        "tv__title",
        "tv__themoviedb_id",
        "tv__imdb_id",
        "tv__original_title",
    )
    list_display = (
        "show",
        "name",
        "tmdb_season_id",
        "season_number",
        "episode_count"
    )
    list_filter = (
        "season_number",
    )
    list_per_page = 200
    list_max_show_all = 1000
    date_hierarchy = "air_date"

    @admin.display(description="TV Show")
    def show(self, obj):
        return obj.tv.title
# common models


class DisplayGenre(admin.ModelAdmin):
    list_display = (
        "num_movie",
        "num_tv",
    )
    search_fields = (
        "name",
    )
    list_filter = (
        "name",
    )

    @admin.display(description="Movies")
    def num_movie(self, obj):
        return obj.movie.count()

    @admin.display(description="TV Shows")
    def num_tv(self, obj):
        return obj.tv.count()


class DisplayCast(admin.ModelAdmin):
    list_display = (
        "name",
        "gender",
        "popularity",
    )
    list_filter = (
        "gender",
    )
    search_fields = (
        "name",
        "movie__title",
        "tv__title",
    )

    @admin.display(description="Movies")
    def num_movie(self, obj):
        return obj.movie.count()

    @admin.display(description="TV Shows")
    def num_tv(self, obj):
        return obj.tv.count()


class DisplayStatus(admin.ModelAdmin):
    list_display = (
        "name",
        "num_movie",
        "num_tv",
    )
    list_filter = (
        "name",
    )

    @admin.display(description="Movies")
    def num_movie(self, obj):
        return obj.movie.count()

    @admin.display(description="TV Shows")
    def num_tv(self, obj):
        return obj.tv.count()


class DisplayType(admin.ModelAdmin):
    list_display = (
        "name",
        "num_tv",
    )
    list_filter = (
        "name",
    )

    @admin.display(description="TV Shows")
    def num_tv(self, obj):
        return obj.tv.count()


class DisplayReport(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "description",
        "reported",
    )
    search_fields = (
        "movie__title",
        "episode__name",
    )
    list_filter = (
        "status",
    )
    date_hierarchy = "added_on"

    def reported(self, obj):
        return f"{timesince.timesince(obj.added_on)} ago"

    def title(self, obj):
        return obj.__str__()


class DisplayPage(admin.ModelAdmin):
    list_display = (
        "title",
        "order",
    )


class DisplayConfiguration(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "themoviedb_api_key",
    )


admin.site.register(Movie, DisplayMovie)
admin.site.register(TV, DisplayTV)
admin.site.register(WatchMovie, DisplayWatchMovie)
admin.site.register(WatchEpisode, DisplayWatchEpisode)
admin.site.register(Episode, DisplayEpisode)
admin.site.register(Season, DisplaySeason)
admin.site.register(EpisodeSubtitle, DisplayEpisodeSubtitle)
admin.site.register(MovieSubtitle, DisplayMovieSubtitle)
admin.site.register(Genre, DisplayGenre)
admin.site.register(Cast, DisplayCast)
admin.site.register(Status, DisplayStatus)
admin.site.register(Type, DisplayType)
admin.site.register(Report, DisplayReport)
admin.site.register(Page, DisplayPage)
admin.site.register(Configuration)
admin.site.register(CustomUser, CustomUserAdmin)
