from django.shortcuts import render

def landing_page(request):
    return render(request, "land.html")

def no_access(request):
    return render(request, "no_access.html")
