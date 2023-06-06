from django.shortcuts import render
from .models import content
from accounts.models import *
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request,'photofetcher/base.html',{'fno':1})



