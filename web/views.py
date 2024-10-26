from django.shortcuts import render,redirect
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import status
import logging
import uuid
from django.conf import settings
import redis

error_dict = {'is_error':False}

logger = logging.getLogger(__name__)
session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

@api_view(["POST"])
def api_register_user(request):
    logger.error(request.user)

    try:
        if request.COOKIES["session_id"] is not None:
            return Response({'status': 'Уже в системе'}, status=status.HTTP_403_FORBIDDEN)
    except:
        if CustomUser.objects.filter(username = request.data['username']).exists(): 
            return Response({'status': 'Exist'}, status=400)
        serializer = UserRegSerializer(data=request.data) 
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def api_login_user(request):
    try:
        if request.COOKIES["session_id"] is not None:
            return Response({'status': 'Уже в системе'}, status=status.HTTP_403_FORBIDDEN)
    except:
        username = str(request.data["username"]) 
        password = request.data["password"]
        logger.error(f'{username} -> {password}')
        user = authenticate(request, username=username, password=password)
        logger.error(user) 
        if user is not None:
            random_key = str(uuid.uuid4()) 
            session_storage.set(random_key, username)

            response = Response({'status': f'{username} успешно вошел в систему'})
            response.set_cookie("session_id", random_key)

            return response
        else:
            return HttpResponse("{'status': 'error', 'error': 'login failed'}")

@api_view(["GET"])
def api_info_user(request, pk):
    user = CustomUser.objects.filter(pk=pk)
    serializer = UserRegSerializer(user)
    return Response(serializer.data)


def login_user(request):
    global error_dict
    return render(request, 'login.html', error_dict)

def check_login_user(request):
    global error_dict
    try:
        if request.COOKIES("session_id") is not None:
            error_dict['is_error'] = True
            return redirect("user", "login")
    except:
        username = str(request.POST.get("login")) 
        password = request.POST.get("pass")
        logger.error(f'{username} -> {password}')
        user = authenticate(request, username=username, password=password)
        logger.error(user) 
        if user is not None:
            random_key = str(uuid.uuid4()) 
            session_storage.set(random_key, username)

            response = redirect("/home")
            response.set_cookie("session_id", random_key)

            return response
        else:
            error_dict['is_error'] = True
            return redirect("/user/login")
        
def home(request):
    global error_dict
    error_dict['is_error'] = False

    # name_org = request.GET.get('name_org')
    # orgs = event.objects.filter(name__icontains=name_org)


    return render(request, 'home.html')