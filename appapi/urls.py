from django.urls import path
from . import views
from . import dramaAPIViews
from django.views.generic import RedirectView
from django.views.decorators.cache import cache_page
app_name = "app_appapi"
urlpatterns = [
    path("params/",views.ConfigAPIView.as_view(),name="params"),# cache for 1 hour
    path("settings/",views.ConfigAPIView.as_view(),name="settings"),#cache for 1 hour
    path("search/<str:query>/",views.SearchAPIView.as_view(),name="search"),
    path("series/show/<int:pk>/",views.SerieAPIView.as_view(),name="serie"),
    path("media/detail/<int:pk>/",views.MovieAPIView.as_view(),name="movie"),
    path("series/relateds/<int:pk>/",cache_page(60*60*24)(views.RelatedSerieAPIView.as_view()),name="related_series"),#cache for 1 day
    path("media/relateds/<int:pk>/",cache_page(60*60*24)(views.RelatedMovieAPIView.as_view()),name="related_movies"),
    path("media/suggestedcontent/",cache_page(60*60*24)(views.SuggestedContentAPIView.as_view()),name="suggested_content"),
    path("genres/list/",cache_page(60*60*24*7)(views.AllGenreAPIView.as_view()),name="genres"),
    path("media/recommendedcontent/",cache_page(60*60*24)(views.RecommendedAPIView.as_view()),name="recommended"),
    path("media/featuredcontent/",cache_page(60*60*24)(views.FeaturedAPIView.as_view()),name="featured"),
    path("media/topcontent/",cache_page(60*60*24*4)(views.TOP10APIView.as_view()),name="top_content"),# cache for 4 days
    path("media/latestcontent/",views.LatestReleaseAPIView.as_view(),name="latest_releases"),
    path("series/recentscontent/",views.LatestSerieAPIView.as_view(),name="latest_series"),
    path("series/popular/",cache_page(60*60*24)(views.PopularSerieAPIView.as_view()),name="popular_series"),
    path("media/popularcontent/",cache_page(60*60*24)(views.PopularMovieAPIView.as_view()),name="popular_movies"),
    path("series/newEpisodescontent/",views.NewEpisodeAPIView.as_view(),name="new_episodes"),
    path("animes/recents/",views.LatestAnimeAPIView.as_view(),name="latest_animes"),
    path("genres/topteen/all/",cache_page(60*60*24*4)(views.GenreTop10APIView.as_view()),name="genre_top10"),
    path("genres/new/all/",views.GenreNewAPIView.as_view(),name="genre_new"),
    path("genres/popularmovies/all/",cache_page(60*60*24)(views.GenrePopularMovieAPIView.as_view()),name="popular_movies"),
    path("media/thisweekcontent/",views.NewThisWeekAPIView.as_view(),name="new_this_week"),
    path("genres/thisweek/all/",views.NewThisWeekGenreAPIView.as_view(),name="genre_this_week"),
    path("series/episodeshow/<int:pk>/",views.EpisodeShowAPIView.as_view(),name="episode_show"),
    path("genres/movies/all/",cache_page(60*60*24)(views.MoviesAPIView.as_view()),name="movies"),
    path("genres/series/all/",cache_page(60*60*24)(views.SeriesAPIView.as_view()),name="series"),
    path("media/choosedcontent/",cache_page(60*60*24)(views.ChoosedAPIView.as_view()),name="choosed"),
    path("genres/choosed/all/",cache_page(60*60*24)(views.ChoosedGenreAPIView.as_view()),name="choosed_genre"),
    path("media/seriesEpisodesAll/",views.GenreLatestEpisodeAPIView.as_view(),name="genre_latest_episode"),
    path("genres/recommended/all/",cache_page(60*60*24)(views.GenreRecommendedAPIView.as_view()),name="genre_recommended"),
    path("genres/popularseries/all/",cache_page(60*60*24)(views.GenrePopularSerieAPIView.as_view()),name="genre_popular"),
    path("media/trendingcontent/",cache_page(60*60*24)(views.TrendingThisWeekAPIView.as_view()),name="trending_content"),
    path("genres/trending/all/",cache_page(60*60*24)(views.GenreTrendingAPIView.as_view()),name="genre_trending"),
    path("movies/<str:filter>/",cache_page(60*60*24)(views.FilterMovieByNonGenreAPIView.as_view()),name="filter_movie_by_non_genre"),
    path("genres/movies/show/<int:genre_id>/",cache_page(60*60*24)(views.MovieByGenreAPIView.as_view()),name="movie_by_genre"),
    path("series/<str:filter>/",cache_page(60*60*24)(views.FilterTVByNonGenreAPIView.as_view()),name="filter_tv_by_non_genre"),
    path("genres/series/show/<int:genre_id>/",cache_page(60*60*24)(views.TVByGenreAPIView.as_view()),name="tv_by_genre"),
    path("genres/series/showPlayer/<int:genre_id>/",cache_page(60*60*24)(views.TVByGenreAPIView.as_view()),name="show_player_genre"),
    path("genres/latestseries/all/",views.GenreLatestSerieAPIView.as_view(),name="genre_latest_serie"),
    path("register/",views.RegisterAPIView.as_view(),name="register_api"),
    path("report/",views.SuggestAPIView.as_view(),name="report_api"),
    path("user/",views.UserAPIView.as_view(),name="user_api"),
    path("account/update/",views.UpdateAccountAPIView.as_view(),name="update_account_api"),
    path("login/",views.LoginAPIView.as_view(),name="login_api"),
    path("upcoming/latest/",views.UpcomingAPIView.as_view(),name="upcoming_api"),
    # path("account/isSubscribed/",views.IsSubscribedAPIView.as_view(),name="isSubscribed_api"),
    path("suggest/",views.SuggestAPIView.as_view(),name="suggest_api"),
    # path("image/minilogo",RedirectView()),
    # path("categories/list/<str:userID>",views.AllGenreAPIView.as_view(),name="categories"),
    path("",dramaAPIViews.home,name="home"),
    path("watch/",dramaAPIViews.watch,name="watch"),
]