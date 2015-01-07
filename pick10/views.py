from django.shortcuts import render

from pick10.models import Team

def home(request):
    return render(request, 'pick10/home.html')

