from django.conf import settings
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=254)
    age_years = models.IntegerField()
    age_months = models.IntegerField()
    age_days = models.IntegerField()

