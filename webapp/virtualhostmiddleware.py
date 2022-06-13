
class VirtualHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host in "www.watchcool.in":
            request.urlconf = "watchcool.webapp_urls"
        else:
            request.urlconf = "watchcool.api_urls"
        response = self.get_response(request)
        return response