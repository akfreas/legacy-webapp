from django.conf import settings
from django.db import models


class Figure(models.Model):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100)
    image_url = models.URLField(blank=True)

class Event(models.Model):
    figure = models.ForeignKey("Figure", null=True)
    description = models.CharField(max_length=254)
    male = models.BooleanField()
    age_years = models.IntegerField()
    age_months = models.IntegerField()
    age_days = models.IntegerField()

class EventUser(models.Model):

    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    facebook_id = models.CharField(max_length=200)
    date_first_seen = models.DateField(null=True)
    date_last_seen = models.DateField(null=True)
    num_requests = models.IntegerField(null=True)
