from django.shortcuts import render

# Create your views here.

def Home(request):
    return render(request, 'create.html')

def Home1(request):
    return render(request, 'home.html')

def Home2(request):
    return render(request, 'description.html')

def Home3(request):
    return render(request, 'reg.html')
