from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import requests
import re
from webapp.models import Configuration
BASE_DIR = Path(__file__).resolve().parent
def get_realtime_user():
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    KEY_FILE_LOCATION = BASE_DIR/'config/analytics-api-328702-10cd9ecce22b.json'
    VIEW_ID="252928379"
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Create requests session object (avoids need to pass in headers with every request)
    session = requests.Session()
    session.headers= {'Authorization': 'Bearer ' + credentials.get_access_token().access_token}

    # Enjoy!
    url_kwargs = {
        'view_id': VIEW_ID,  # Can be obtained from here: https://ga-dev-tools.appspot.com/account-explorer/
        'get_args': 'metrics=rt:activeUsers'  # https://developers.google.com/analytics/devguides/reporting/realtime/v3/reference/data/realtime/get
    }
    response = session.get('https://www.googleapis.com/analytics/v3/data/realtime?ids=ga:{view_id}&{get_args}'.format(**url_kwargs))
    response.raise_for_status()
    result = response.json()
    return result["totalsForAllResults"].get("rt:activeUsers",0)
def getMeta(tmdbid,themoviedb_api_key,media_type="movie"):
    tmdb_base_url = f"https://api.themoviedb.org/3/{media_type}/{tmdbid}?api_key={themoviedb_api_key}&language=en-US&append_to_response=videos"
    base_resp = requests.get(tmdb_base_url)
    if base_resp.status_code == 200:
        response_data = base_resp.json()
        return response_data
def search(title,themoviedb_api_key,year=None):
    tmdb_base_url = f"https://api.themoviedb.org/3/search/multi?api_key={themoviedb_api_key}&language=en-US&page=1&query={title}{'&year='+year if year else ''}&include_adult=true"
    if not year:
        resp_data = sorted(requests.get(tmdb_base_url).json().get("results",[]),key=lambda a:a.get("popularity",0.0),reverse=True)
    else:
        resp_data = requests.get(tmdb_base_url).json().get("results",[])
    if resp_data:
        return resp_data[0].get("id")
def getSeason(tmdbid,season_number,themoviedb_api_key):
    tmdb_base_url = f"https://api.themoviedb.org/3/tv/{tmdbid}/season/{season_number}?api_key={themoviedb_api_key}&language=en-US"
    resp = requests.get(tmdb_base_url)
    if resp.status_code == 200:
        return resp.json()
def getEpisode(tmdbid,season_number,episode_number,themoviedb_api_key):
    tmdb_base_url = f"https://api.themoviedb.org/3/tv/{tmdbid}/season/{season_number}/episode/{episode_number}?api_key={themoviedb_api_key}&language=en-US"
    resp = requests.get(tmdb_base_url)
    if resp.status_code == 200:
        return resp.json()
def getConfig():
    return Configuration.objects.first()
def extractEpisodeNum(url):
    episodeNum = re.search(r"\b[\d]{1,3}(-[\d])?\b",url)
    if episodeNum:
        return episodeNum.group().replace("-",".")
    return "0"
    