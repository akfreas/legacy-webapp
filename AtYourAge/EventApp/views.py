from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core import serializers
from django.db.models import F

from datetime import datetime

from EventApp.models import *
from EventApp import settings

import json

import utils

def event(request, years, months, days):
    event = Event.objects.filter(age_years=years, age_months=months, age_days=days)
    response = serializers.serialize("json", event) 
    return HttpResponse(response)

def event_with_birthday(request, fb_id, year, month, day):    

    elapsed_time = utils.get_age(int(year), int(month), int(day))

    years = elapsed_time["years"]
    months = elapsed_time["months"]
    days = elapsed_time["days"]

    try:
        user = EventUser.objects.get(facebook_id=fb_id)
    except EventUser.DoesNotExist:
        user = EventUser(facebook_id=fb_id)
        user.date_first_seen = datetime.now()

    user.date_last_seen = datetime.now()
    user.num_requests = 1
    user.save()
    

    events = Event.objects.filter(age_years=years, age_months=months, age_days=days)
    event_list = []
    for event in events: 
        response_dict = {'age_years' : event.age_years, 
                'age_months' : event.age_months,
                'age_days' : event.age_days,
                'male' : event.male,
                'description' : event.description,
                'name' : event.name }
        event_list.append(response_dict)
    response = json.dumps(event_list)

    return HttpResponse(response)
