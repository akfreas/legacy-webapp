from django.template import RequestContext, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.core import serializers
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt


from datetime import datetime

from EventApp.models import *
from EventApp import settings

import json

import utils

def event(request, years, months, days):
    event = Event.objects.filter(age_years=years, age_months=months, age_days=days)
    response = serializers.serialize("json", event) 
    return HttpResponse(response)

@csrf_exempt
def test(request):
    print request
    return render_to_response("base.html")

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
                'name' : event.name,
                'story_html'  :"<html><body>HEY MAN</body></html>" }
        event_list.append(response_dict)
    response = json.dumps(event_list)

    return HttpResponse(response)

def story_with_birthday(request, fb_id, year, month, day):

    elapsed_time = utils.get_age(int(year), int(month), int(day))

    years = elapsed_time["years"]
    months = elapsed_time["months"]
    days = elapsed_time["days"]

    formatted_cookie = request.COOKIES['AtYourAge'].replace("'", "\"")
    user_dict = json.loads(formatted_cookie)

    access_token = user_dict['token']
    user_id = user_dict['activeUserId']


    try:
        user = EventUser.objects.get(facebook_id=fb_id)
    except EventUser.DoesNotExist:
        user = EventUser(facebook_id=fb_id)
        user.date_first_seen = datetime.now()
        utils.populate_user_with_fb_fields(user, access_token)
        user.save()

    try:
        requesting_user = EventUser.objects.get(facebook_id=user_id)
        requesting_user.date_last_seen = datetime.now()
        requesting_user.num_requests = requesting_user.num_requests + 1
        requesting_user.save()
    except EventUser.DoesNotExist:
        pass
    

    events = Event.objects.filter(age_years=years, age_months=months, age_days=days)
    event_list = []
    print request.COOKIES 
    event = events[0]

    person_profile_pic = utils.person_profile_pic(fb_id, access_token)
    figure_profile_pic = utils.figure_profile_pic(event)
    figure_wikipedia_pic = utils.figure_wikipedia_pic(event.name, 200)
    print figure_wikipedia_pic
    if len(figure_wikipedia_pic) > 0:
        figure_wikipedia_pic = figure_wikipedia_pic[0]
    else:
        figure_wikipedia_pic = figure_profile_pic  #BAD STUFF MAN, HANDLE YOUR ERRORS

    event = events[0]
    sex = "he"
 
    if event.male == False:
        sex = "she"
   
    description = "%s" % (event.description.capitalize(),)

    info_dict = {'person_profile_pic' : person_profile_pic,
            'figure_profile_pic' : figure_wikipedia_pic['url'],
            'figure_name' : event.name,
            'age_years' : years,
            'age_months' : months,
            'age_days' : days,
            'figure_pronoun' : sex,
            'figure_event' : description,}

    response = json.dumps(info_dict)

    return HttpResponse(response)




#    return render_to_response("base.html", info_dict)
