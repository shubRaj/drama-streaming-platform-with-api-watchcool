from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import requests
from .playdrive import PlayDrive
from operator import itemgetter
from urllib.parse import urlparse
import asyncio
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
def remoteUploadFembed(api_key,url):
    parsedUrl = urlparse(url)
    fembed_url = f"https://fembed.com{parsedUrl.path}"
    data = asyncio.run(PlayDrive(api_key).upload(fembed_url))
    return data
def getDirectLinks(slug):
    links = asyncio.run(PlayDrive().getDirectLinks(f"https://player.watchcool.in/d/{slug}/"))
    return links
