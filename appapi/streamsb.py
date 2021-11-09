import requests
import string
import re
import random
from urllib.parse import urlparse
from django.core.cache import cache

def getStreamSBSource(streamsb_url):
    if streamsb_url.endswith(".html"):
        id = re.split("/|\.", urlparse(streamsb_url).path)[-2]
    else:
        id = re.split("/|\.", urlparse(streamsb_url).path)[-1]
    stream_url = cache.get(f"streamsb_{id}")
    try:
        if not stream_url:
            char = string.ascii_letters+string.digits
            first_identifier = f"{''.join(random.choices(char,k=5))}streamsb1@{''.join(random.choices(char,k=5))}@{id}@streamsb2".encode("utf-8").hex()
            s = requests.Session()
            resp_data = s.get(f"https://playersb.com/sources/{first_identifier}/{first_identifier}", headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                "Xstreamsb": "sbembed",
            }).json()
            stream_data = resp_data.get("stream_data")
            if stream_data:
                parsed_url = urlparse(stream_data.get("backup"))
                stream_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
                s.head(stream_url)
                cache.set(f"streamsb_{id}",stream_url,60*60*3)
    except:
        pass
    return stream_url