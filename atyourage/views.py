from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core import serializers

from atyourage.models import Event
from atyourage import settings

import utils

def event(request, years, months, days):
    event = Event.objects.filter(age_years=years, age_months=months, age_days=days)
    response = serializers.serialize("json", event) 
    return HttpResponse(response)

def event_with_birthday(request, month, day, year):
    
    elapsed_time = utils.get_age(int(year), int(month), int(day))

    years = elapsed_time[0]
    months = elapsed_time[1]
    days = elapsed_time[2]

    event = Event.objects.filter(age_years=years, age_months=months, age_days=days)
    
    response = serializers.serialize("json", event)

    return HttpResponse(response)
