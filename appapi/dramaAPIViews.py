from django.http import JsonResponse, HttpResponseRedirect
from django.core.cache import cache
from urllib import parse
import json
import re
from .streamsb import getSource
from .asianload import getSource as getAsianloadSource
def home(request):
    source = request.GET.get("source")
    if source and source.startswith("https://"):
        parsed_url = parse.urlparse(source)
        if "sb" in parsed_url.netloc:
            if source.endswith(".html"):
                id = re.split("/|\.", parse.urlparse(source).path)[-2]
            else:
                id = re.split("/|\.", parse.urlparse(source).path)[-1]
            data = cache.get(f"streamsb_{id}")
            if not data:
                stream_data = getSource(source)
                if stream_data:
                    for key in ["hash", "length", "logo", "cdn_img"]:
                        stream_data.pop(key)
                    data = {
                        "source": [stream_data]
                    }
                    cache.set(f"streamsb_{id}", data, 60*60*3)
            return JsonResponse(data)
        elif "asian" in parsed_url.netloc:
            id = parse.parse_qs(parsed_url.query)["id"][0]
            data = cache.get(f"asianload_{id}")
            if not data:
                stream_data = getAsianloadSource(id)
                if stream_data:
                    stream_data["backup"] = stream_data.pop("url")
                    data = {
                        "source":[stream_data],
                    }
                    cache.set(f"asianload_{id}",data,60*60*3)
            return JsonResponse(data)
    return JsonResponse({"message": "Wink Wink"}, status=400)


def watch(request):
    resp = home(request)
    if resp.status_code == 200:
        media = json.loads(resp.content.decode()).get("source", [])
        for source in media:
            return HttpResponseRedirect(source.get("backup"))
    return resp
