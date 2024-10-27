from django.db import models
from django.contrib.auth.models import User, UserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
 

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        if not username:
            raise ValueError('Username обязателен')
    
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):     
    username = models.CharField(unique=True, max_length=150)
    email = models.CharField(max_length=254, unique=True, verbose_name="Email")
    password = models.CharField(max_length=254, verbose_name="Пароль")
    last_login = models.DateTimeField(blank=True, null=True)

    is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")
    sex = models.CharField(default=None, max_length=10, verbose_name="Пол", null=True, blank=True)
    board_games = models.FloatField(default=0, verbose_name="Отношение к настольным играм")
    arts = models.FloatField(default=0, verbose_name="Отношение к искусству")
    sport = models.FloatField(default=0, verbose_name="Отношение к спорту")
    nature = models.FloatField(default=0, verbose_name="Отношение к природе")
    food = models.FloatField(default=0, verbose_name="Отношение к еде")

    duration = models.FloatField(default=0, verbose_name="Предпочтительное время мероприятий")
    capacity = models.FloatField(default=0, verbose_name="Предпочтительное количество мест")

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'  
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.username

    class Meta:
        managed = True
        db_table = 'custom_user'


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'category'

class event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="Descr")
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
