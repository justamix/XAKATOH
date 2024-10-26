from django.shortcuts import render
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
import numpy as np
# from utils import cosine_distance
from .utils import cosine_distance

logger = logging.getLogger(__name__)
session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

@api_view(["POST"])
def register_user(request):
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
def login_user(request):
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

def home(request):
    user_id = 0
    return HttpResponse('Hello world!')

def get_user_factors(user):
    factors = [user.board_games, user.arts, user.sport, user.nature, user.food, user.duration, user.capacity] #TODO: add sex, age
    userbody = np.array(factors)
    return userbody

def get_user_event_factors(user):
    factors = [user.board_games, user.arts, user.sport, user.nature, user.food, user.duration, user.capacity] #TODO: check order
    return np.array(factors)

def get_event_factors(event):
    cat = event.category
    one_hot_category = np.ones((5))
    one_hot_category[cat] = 1
    factors = np.hstack(one_hot_category, np.array([event.duration, event.capacity]))
    return factors

def get_reqs(user_id):
    users = models.CustomUser.objects
    events = models.event.objects
    user = models.CustomUser.objects
    userbody = get_user_factors(user_id)
    event_factors = get_user_event_factors(user)
    similar_users = list(sorted(users, key=lambda x: cosine_distance(get_user_factors(x), userbody)))[::-1][min(5, len(users))]
    similar_events = list(sorted(events, key=lambda x: cosine_distance(get_event_factors(x), event_factors)))[::-1][:min(5, len(events))]
    similar_users_events = []

    for user in similar_users:
        top_events = models.EventUser.objects.filter(user=user)
        similar_users_events.extend([mm.event for mm in top_events])
    return similar_events + similar_users_events



    
    