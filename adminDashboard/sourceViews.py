from webapp.models import Episode
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
                    tv_title = tv_title.replace(punc,"")
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
                print(episodes)
                episode.source_url=episodes[episode.episode_number-1]
                print(episode)
                episode.save()
            except Exception as e:
                print(e)
    return {"hi":"hi"}