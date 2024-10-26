from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse('Hello world!')
