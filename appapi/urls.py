from django.urls import path
from . import views
from . import dramaAPIViews
from django.views.generic import RedirectView
from django.conf import settings
from django.views.decorators.cache import cache_page
app_name = "app_appapi"
urlpatterns = [
    path("settings/",cache_page(settings.CACHE_TIME)(views.ConfigAPIView.as_view()),name="settings"),
    path("search/<str:query>/",cache_page(settings.CACHE_TIME)(views.SearchAPIView.as_view()),name="search"),
    path("series/show/<int:pk>/",views.SerieAPIView.as_view(),name="serie"),
    path("media/detail/<int:pk>/",views.MovieAPIView.as_view(),name="movie"),
    path("series/relateds/<int:pk>/",cache_page(settings.CACHE_TIME)(views.RelatedSerieAPIView.as_view()),name="related_series"),
    path("media/relateds/<int:pk>/",cache_page(settings.CACHE_TIME)(views.RelatedMovieAPIView.as_view()),name="related_movies"),
    path("media/suggestedcontent/",cache_page(settings.CACHE_TIME)(views.SuggestedContentAPIView.as_view()),name="suggested_content"),
    path("genres/list/",cache_page(settings.CACHE_TIME)(views.AllGenreAPIView.as_view()),name="genres"),
    path("media/recommendedcontent/",cache_page(settings.CACHE_TIME)(views.RecommendedAPIView.as_view()),name="recommended"),
    path("media/featuredcontent/",cache_page(settings.CACHE_TIME)(views.FeaturedAPIView.as_view()),name="featured"),
    path("media/topcontent/",cache_page(settings.CACHE_TIME)(views.TOP10APIView.as_view()),name="top_content"),
    path("media/latestcontent/",cache_page(settings.CACHE_TIME)(views.LatestReleaseAPIView.as_view()),name="latest_releases"),
    path("series/recentscontent/",cache_page(settings.CACHE_TIME)(views.LatestSerieAPIView.as_view()),name="latest_series"),
    path("series/popular/",cache_page(settings.CACHE_TIME)(views.PopularSerieAPIView.as_view()),name="popular_series"),
    path("media/popularcontent/",cache_page(settings.CACHE_TIME)(views.PopularMovieAPIView.as_view()),name="popular_movies"),
    path("series/newEpisodescontent/",cache_page(settings.CACHE_TIME)(views.NewEpisodeAPIView.as_view()),name="new_episodes"),
    path("animes/recents/",cache_page(settings.CACHE_TIME)(views.LatestAnimeAPIView.as_view()),name="latest_animes"),
    path("genres/topteen/all/",cache_page(settings.CACHE_TIME)(views.GenreTop10APIView.as_view()),name="genre_top10"),
    path("genres/new/all/",cache_page(settings.CACHE_TIME)(views.GenreNewAPIView.as_view()),name="genre_new"),
    path("genres/popularmovies/all/",cache_page(settings.CACHE_TIME)(views.GenrePopularMovieAPIView.as_view()),name="popular_movies"),
    path("media/thisweekcontent/",cache_page(settings.CACHE_TIME)(views.NewThisWeekAPIView.as_view()),name="new_this_week"),
    path("genres/thisweek/all/",cache_page(settings.CACHE_TIME)(views.NewThisWeekGenreAPIView.as_view()),name="genre_this_week"),
    path("series/episodeshow/<int:pk>/",views.EpisodeShowAPIView.as_view(),name="episode_show"),
    path("genres/movies/all/",cache_page(settings.CACHE_TIME)(views.MoviesAPIView.as_view()),name="movies"),
    path("genres/series/all/",cache_page(settings.CACHE_TIME)(views.SeriesAPIView.as_view()),name="series"),
    path("media/choosedcontent/",cache_page(settings.CACHE_TIME)(views.ChoosedAPIView.as_view()),name="choosed"),
    path("genres/choosed/all/",cache_page(settings.CACHE_TIME)(views.ChoosedGenreAPIView.as_view()),name="choosed_genre"),
    path("media/seriesEpisodesAll/",cache_page(settings.CACHE_TIME)(views.GenreLatestEpisodeAPIView.as_view()),name="genre_latest_episode"),
    path("genres/recommended/all/",cache_page(settings.CACHE_TIME)(views.GenreRecommendedAPIView.as_view()),name="genre_recommended"),
    path("genres/popularseries/all/",cache_page(settings.CACHE_TIME)(views.GenrePopularSerieAPIView.as_view()),name="genre_popular"),
    path("media/trendingcontent/",cache_page(settings.CACHE_TIME)(views.TrendingThisWeekAPIView.as_view()),name="trending_content"),
    path("genres/trending/all/",cache_page(settings.CACHE_TIME)(views.GenreTrendingAPIView.as_view()),name="genre_trending"),
    path("movies/<str:filter>/",cache_page(settings.CACHE_TIME)(views.FilterMovieByNonGenreAPIView.as_view()),name="filter_movie_by_non_genre"),
    path("genres/movies/show/<int:genre_id>/",cache_page(settings.CACHE_TIME)(views.MovieByGenreAPIView.as_view()),name="movie_by_genre"),
    path("series/<str:filter>/",cache_page(settings.CACHE_TIME)(views.FilterTVByNonGenreAPIView.as_view()),name="filter_tv_by_non_genre"),
    path("genres/series/show/<int:genre_id>/",cache_page(settings.CACHE_TIME)(views.TVByGenreAPIView.as_view()),name="tv_by_genre"),
    path("genres/series/showPlayer/<int:genre_id>/",cache_page(settings.CACHE_TIME)(views.TVByGenreAPIView.as_view()),name="show_player_genre"),
    path("genres/latestseries/all/",cache_page(settings.CACHE_TIME)(views.GenreLatestSerieAPIView.as_view()),name="genre_latest_serie"),
    path("media/popularCasters/",cache_page(settings.CACHE_TIME)(views.PopularCastersAPIView.as_view()),name="popular_casters"),
    path("genres/allCasters/all/",cache_page(settings.CACHE_TIME)(views.PopularCastersGenreAPIView.as_view()),name="popular_casters_genre"),
    path("cast/detail/<int:pk>/",cache_page(settings.CACHE_TIME)(views.CastDetailAPIView.as_view()),name="cast_detail_api_view"),
    path("filmographie/detail/<int:pk>/",cache_page(settings.CACHE_TIME)(views.FilmographeAPIView.as_view()),name="filmographe_api_view"),
    path("register/",views.RegisterAPIView.as_view(),name="register_api"),
    path("report/",views.SuggestAPIView.as_view(),name="report_api"),
    # path("user/",views.UserAPIView.as_view(),name="user_api"),
    path("account/update/",views.UpdateAccountAPIView.as_view(),name="update_account_api"),
    path("login/",views.LoginAPIView.as_view(),name="login_api"),
    path("upcoming/latest/",views.UpcomingAPIView.as_view(),name="upcoming_api"),
    # path("account/isSubscribed/",views.IsSubscribedAPIView.as_view(),name="isSubscribed_api"),
    path("suggest/",views.SuggestAPIView.as_view(),name="suggest_api"),
    # path("image/minilogo",RedirectView()),
    # path("categories/list/<str:userID>",views.AllGenreAPIView.as_view(),name="categories"),
    # path("",dramaAPIViews.home,name="home"),
    # path("watch/",dramaAPIViews.watch,name="watch"),
]