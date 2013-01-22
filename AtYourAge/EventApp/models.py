from django.conf import settings
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=254)
    male = models.BooleanField()
    age_years = models.IntegerField()
    age_months = models.IntegerField()
    age_days = models.IntegerField()

class EventUser(models.Model):
    facebook_id = models.CharField(max_length=200)
    date_first_seen = models.DateField()
    date_last_seen = models.DateField()
    num_requests = models.IntegerField()
