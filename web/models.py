from django.db import models
from django.contrib.auth.models import User, UserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):     
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(max_length=254, unique=True)
    password = models.CharField(max_length=254, verbose_name="Пароль")    
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")
    sex = models.CharField(default=None, max_length=10, verbose_name="Пол")
    board_games = models.FloatField(default=0, verbose_name="Отношение к настольным играм")
    arts = models.FloatField(default=0, verbose_name="Отношение к исскуству")
    sport = models.FloatField(default=0, verbose_name="Отношение к спорту")
    nature = models.FloatField(default=0, verbose_name="Отношение к природе")
    food = models.FloatField(default=0, verbose_name="Отношение к еде")

    duration = models.FloatField(default=0, verbose_name="Предпочтительное время мероприятий")
    capacity = models.FloatField(default=0, verbose_name="Предпочтительное кол-во мест")
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)


    def __str__(self):
        return f'{self.username}'

    class Meta:
        managed = True
        db_table = 'custom_user'


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'category'

class event(models.Model):
    date = models.DateTimeField()
    playground = models.CharField(max_length=100)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    address = models.CharField(max_length=100)
    is_open = models.BooleanField(default=True)
    duration_in_minutes = models.IntegerField(default=60)
    capacity = models.IntegerField()
    category = models.ForeignKey('category', models.DO_NOTHING)

    class Meta:
        managed = False 
        db_table = 'event'


class EventUser(models.Model):
    event = models.ForeignKey('event', models.DO_NOTHING)
    user = models.ForeignKey('CustomUser', models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'event_user'
        unique_together = (('event', 'user'),)
