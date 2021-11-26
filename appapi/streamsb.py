import requests
import string
import re
import random
from urllib.parse import urlparse
def getSource(streamsb_url):
    if streamsb_url.endswith(".html"):
        id = re.split("/|\.", urlparse(streamsb_url).path)[-2]
    else:
        id = re.split("/|\.", urlparse(streamsb_url).path)[-1]
    streamsb_parsed_url = urlparse(streamsb_url)
    char = string.ascii_letters+string.digits
    first_identifier = f"{''.join(random.choices(char,k=5))}||{id}||{''.join(random.choices(char,k=5))}||streamsb".encode("utf-8").hex()
    s = requests.Session()
    resp_data = s.get(f"https://playersb.com/sources/{first_identifier}/{first_identifier}", headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        "watchsb": "streamsb",
    }).json()
    stream_data = resp_data.get("stream_data")
    if stream_data:
        parsed_url = urlparse(stream_data.get("file"))
        stream_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        # s.head(stream_url)
        parsed_url = urlparse(stream_data.get("backup"))
        backup_stream_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        s.head(backup_stream_url)
        stream_data["file"] = stream_url
        stream_data["id"] = id
        stream_data["backup"] = backup_stream_url
        for sub in stream_data.get("subs",[]):
            sub["file"] = f"{streamsb_parsed_url.scheme}://{streamsb_parsed_url.netloc}{sub['file']}"
        splitted_backup = stream_data['backup'].split(',')
        splitted_file =  stream_data["file"].split(",")
        stream_data["dl"] = f"{splitted_file[0]}{splitted_file[-2]}/{stream_data['title'].replace(' ','-')}.mp4".replace("hls/","")
        stream_data["backup_dl"] = f"{splitted_backup[0]}{splitted_backup[-2]}/{stream_data['title'].replace(' ','-')}.mp4".replace("hls/","")
        return stream_data
if __name__ == "__main__":
    print(getSource("https://embedsb.com/z976yp4utpcj.html"))
