from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField()

    class Meta:
        managed =True
        db_table = 'category'

class event(models.Model):
    date = models.DateTimeField()
    playground = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=100)
    is_open = models.BooleanField(default=True)
    duration_in_minutes = models.IntegerField(default=60)
    capacity = models.IntegerField()
    category = models.ForeignKey('category', models.DO_NOTHING)

    class Meta:
        managed = True 
        db_table = 'event'


class EventUser(models.Model):
    event = models.ForeignKey('event', models.DO_NOTHING)
    user = models.ForeignKey('user', models.DO_NOTHING)
    class Meta:
        managed = True
        db_table = 'event_user'
        constraints = [
            models.UniqueConstraint(fields=['event', 'user'], name='unique_event_user')
        ]

