from django.shortcuts import render

def page_not_found_view(request, exeption):
    return render(request,'/includes/404.html', status=404)

def server_error(request, exeption):
    return render(request,'/includes/500.html', status=500)