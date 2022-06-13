virtual_hosts = {
    "www.watchcool.in":"watchcool.webapp_urls",
    "watchcool.in":"watchcool.webapp_urls",
    "coolapi.watchcool.in":"watchcool.api_urls",
    "myapi.watchcool.in":"watchcool.api_urls",
    "api.watchcool.in":"watchcool.api_urls",
    "localhost:8000":"watchcool.webapp_urls"
}
class VirtualHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        request.urlconf = virtual_hosts.get(host,"watchcool.webapp_urls")
        response = self.get_response(request)
        return response