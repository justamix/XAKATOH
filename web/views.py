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
import numpy as np
# from utils import cosine_distance
from .utils import cosine_distance, filter_str, CAT_INDEX, MAX_DURATION, MAX_CAPACITY, MAX_AGE, SEX_INDEX

error_dict = {'is_error': False}

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
    name_org = request.GET.get('search_event')
    user_id = 1
    if name_org is None:
        name_org = ''
    search_events = search(name_org)
    req_events = get_reqs(user_id)
    data = {
        "req_events": req_events,
        "search_events": search_events,
        "search_event": name_org
    }

    return render(request, 'home.html', data)

# def home(request):
#     user_id = 0
#     return HttpResponse('Hello world!')

def get_user_factors(user):
    factors = [SEX_INDEX[user.sex], user.age / MAX_AGE, user.nature, user.sport, user.board_games, user.arts, user.food, user.duration, user.capacity] #TODO: add sex, age
    userbody = np.array(factors)
    return userbody

def get_user_event_factors(user):
    factors = [user.nature, user.sport, user.board_games, user.arts, user.food, user.duration, user.capacity] #TODO: check order
    # factors = [user.nature, user.sport, user.board_games, user.arts, user.food]
    return np.array(factors)

def get_event_factors(event):
    cat = event.category
    one_hot_category = np.zeros((5))
    one_hot_category[CAT_INDEX[cat.name]] = 1
    factors = np.hstack((one_hot_category, np.array([event.duration_in_minutes / MAX_DURATION, event.capacity / MAX_CAPACITY])))
    return factors

def get_reqs(user_id):
    cur_user = CustomUser.objects.get(id=user_id)
    users = CustomUser.objects.all()
    events = event.objects.all()
    userbody = get_user_factors(cur_user)
    event_factors = get_user_event_factors(cur_user)
    similar_users = list(sorted(users, key=lambda x: cosine_distance(get_user_factors(x), userbody)))[::-1][:min(5, len(users))]
    similar_events = list(sorted(events, key=lambda x: cosine_distance(get_event_factors(x), event_factors)))[::-1][:min(5, len(events))]
    similar_users_events = []
    for user in similar_users:
        top_events = EventUser.objects.filter(user=user)
        similar_users_events.extend([mm.event for mm in top_events if mm.event not in similar_users_events])
    return similar_events + [event_ for event_ in similar_users_events if event_ not in similar_events]
    # return similar_events

def search(text):
    words = filter_str(text).split()
    events = event.objects.all()
    res = []
    for event_ in events:
        c = 0
        for word in words:
            if word[:-2] in filter_str(event_.description):
                c += 1
            if word[:-2] in filter_str(event_.name):
                c += 1.5
        res.append((event_, c))
    return list(i[0] for i in sorted(res, key=lambda x: -x[1]))

def correct_userbody(user, event, r):
    event_factors = get_event_factors(event)
    user_event_factors = get_user_event_factors(user)
    new_factors = user_event_factors + r * event_factors
    update_factors(user, new_factors)

def update_factors(user, factors):
    user.nature = factors[0]
    user.sport = factors[1]
    user.board_games = factors[2]
    user.arts = factors[3]
    user.food = factors[4]
    user.duration = factors[5]
    user.capacity = factors[6]
    user.save()