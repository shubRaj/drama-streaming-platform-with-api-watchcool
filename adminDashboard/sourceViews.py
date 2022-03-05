from webapp.models import Episode,Movie
import requests
import string
def getEpisodes(tv_url):
    return requests.get(f"https://was.watchcool.in/episodes/?url={tv_url}").json()
def home():
    cache_tv = {}
    cache_episodes = {}
    for episode in Episode.objects.select_related("season").filter(source_url=None).all():
        season = episode.season
        if season.air_date:
            season_released = season.air_date.year
            tv = season.tv
            tv_title = season.tv.title
            for punc in string.punctuation:
                if punc in tv_title:
                    tv_title = tv_title.replace(punc," ")
            if tv_url := cache_tv.get(str(tv.id)):
                if episodes := cache_episodes.get(f"{tv.id}_{season.id}"):
                    pass
                else:
                    episodes = getEpisodes(tv_url).get("sources")
                    cache_episodes[f"{tv.id}_{season.id}"] = episodes
            else:
                tv_url = requests.get(f"https://was.watchcool.in/search/?q={tv_title}&year={season_released}").json().get("url")
                cache_tv[f"{tv.id}"] = tv_url
                episodes = getEpisodes(tv_url).get("sources")
                cache_episodes[f"{tv.id}_{season.id}"] = episodes
            try:
                episode.source_url=episodes[episode.episode_number-1]
                print(episode)
                episode.save()
            except Exception as e:
                print(e)
    return {"hi":"hi"}
def movie():
    for movie in Movie.objects.filter(source_url=None):
        movie_title = movie.title
        release_date = movie.release_date
        if release_date:
            for punc in string.punctuation+"·":
                if punc in movie_title:
                    movie_title = movie_title.replace(punc," ")
            movie_url = requests.get(f"https://was.watchcool.in/search/?q={movie_title}&year={release_date.year}").json().get("url")
            episodes = getEpisodes(movie_url).get("sources")
            try:
                movie.source_url = episodes[-1]
                print(movie_title)
                movie.save()
            except Exception as e:
                print(e)