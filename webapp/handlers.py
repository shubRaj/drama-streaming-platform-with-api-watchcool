from django.shortcuts import render
from django.http import JsonResponse
def page_not_found(request,exception):
    return JsonResponse({"message":"Not Found - 404"},status=404)
    # return render(request,"webapp/404.html",{"title":"Page Not Found - 404","description":"page not found"},status=404)
def server_error(request):
    return JsonResponse({"message":"Server Error - 500"},status=500)
    # return render(request,"webapp/500.html",{"title":"Server Error - 500","description":"page not found"},status=500)
def bad_request(request):
    return JsonResponse({"message":"Bad Request - 400"},status=400)