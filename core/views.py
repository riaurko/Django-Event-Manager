from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def landing_page(request):
    return render(request, "land.html")

def no_access(request):
    return render(request, "no_access.html")
