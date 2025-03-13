from django.shortcuts import render
from .models import Influencer

def home (request): 
    return render(request, 'website/index.html')  


# Create your views here.
