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
import random


error_login = {'is_error':False}
error_register = {'is_error':False}

logger = logging.getLogger(__name__)
session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

# add_users()

   
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
    global error_login
    try:
        username = session_storage.get(request.COOKIES["session_id"])
        username = username.decode('utf-8')
        return redirect("/home")
    except:
        return render(request, 'login.html', error_login)

def check_login_user(request):
    global error_login
    try:
        username = session_storage.get(request.COOKIES["session_id"])
        username = username.decode('utf-8')
        return redirect("/home")
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
            error_login['is_error'] = True
            return redirect("/user/login")
        

def register_user(request, is_error=False):
    global error_register
    try:
        username = session_storage.get(request.COOKIES["session_id"])
        username = username.decode('utf-8')
        return redirect("/home")
    except:
        return render(request, 'reg.html', error_register)

def check_register_user(request):
    global error_register

    username = request.POST.get('username')
    email = request.POST.get('email')
    sex = request.POST.get('gender')
    age = int(request.POST.get('age'))
    password = request.POST.get('password')

    logger.error(f"{username}, {email}, {sex}, {age}, {password}")

    try:
        new_user = CustomUser.objects.create_user(
            username = username,
            email = email,
            sex = sex,
            age = age,
            password = password
        )

        return redirect('/user/login')

    except:
        error_register['is_error'] = True
        return redirect('/user/register')

        
def home(request):
    global error_login
    error_login['is_error'] = False
    try:
        username = session_storage.get(request.COOKIES["session_id"])
        username = username.decode('utf-8')
    except:
        return redirect('/user/login')
    my_data = {
        'username': username
    }

    return render(request, 'home.html', my_data)


