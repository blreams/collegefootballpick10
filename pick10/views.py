from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from pick10.models import Team

def home(request):
    return render(request, 'pick10/home.html')

@login_required
def index(request):
    return render(request, 'pick10/index.html')

