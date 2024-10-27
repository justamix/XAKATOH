from django.db import models
from django.contrib.auth.models import User, UserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.conf import settings

class CustomUserManager(BaseUserManager):
    # use_in_migrations = True

    def create_user(self, username, email, password=None, age=None, sex=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        if not username:
            raise ValueError('Username обязателен')
    
        user = self.model(username=username, email=email, age=age, sex=sex, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, age=None, sex=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(username, email, password, age, sex, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):     
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(max_length=254, unique=True, verbose_name="Email")
    password = models.CharField(max_length=254, verbose_name="Пароль")
    sex = models.CharField(default=None, max_length=10, verbose_name="Пол", null=True, blank=True)

    last_login = models.DateTimeField(blank=True, null=True)
    age = models.IntegerField(default=0)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")
    
    board_games = models.FloatField(default=0, verbose_name="Отношение к настольным играм")
    arts = models.FloatField(default=0, verbose_name="Отношение к искусству")
    sport = models.FloatField(default=0, verbose_name="Отношение к спорту")
    nature = models.FloatField(default=0, verbose_name="Отношение к природе")
    food = models.FloatField(default=0, verbose_name="Отношение к еде")

    duration = models.FloatField(default=0, verbose_name="Предпочтительное время мероприятий")
    capacity = models.FloatField(default=0, verbose_name="Предпочтительное количество мест")

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = ['email']  

    def __str__(self):
        return self.username

    class Meta:
        managed = True
        db_table = 'custom_user'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed =True
        db_table = 'category'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

class event(models.Model):
    name = models.TextField()
    description = models.TextField(default="Descr")
    date = models.DateTimeField()
    playground = models.CharField(max_length=100)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    address = models.CharField(max_length=100)
    is_open = models.BooleanField(default=True)
    duration_in_minutes = models.IntegerField(default=60)
    capacity = models.IntegerField()
    category = models.ForeignKey('category', models.DO_NOTHING, verbose_name='category')
    creater = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, default=1, verbose_name='creater')
    url = models.URLField(max_length=200, verbose_name='URL', null=True, blank=True)

    class Meta:
        managed = True 
        db_table = 'event'
        verbose_name = 'мероприятие'
        verbose_name_plural = 'мероприятия'


class EventUser(models.Model):
    event = models.ForeignKey('event', models.DO_NOTHING)
    user = models.ForeignKey('CustomUser', models.DO_NOTHING)
    class Meta:
        managed = True
        db_table = 'event_user'
        unique_together = (('event', 'user'),)
        verbose_name = 'посещение'
        verbose_name_plural = 'посещения'
