from django.shortcuts import render
def page_not_found(request,exception):
    return render(request,"webapp/404.html",{"title":"Page Not Found - 404","description":"page not found"},status=404)
def server_error(request):
    return render(request,"webapp/500.html",{"title":"Server Error - 500","description":"page not found"},status=500)