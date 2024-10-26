from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse
import models
import numpy as np
from utils import cosine_distance

# Create your views here.

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
    similar_users = list(sorted(users, key=lambda x: cosine_distance(get_user_factors(x), userbody)))[::-1]
    similar_events = list(sorted(events, key=lambda x: cosine_distance(get_event_factors(x), userbody)))[::-1][:min(5, len(events))]
    return




    
    