from django.template import RequestContext, loader
from django.http.response import *
from django.shortcuts import render_to_response
from django.core import serializers
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt

from random import sample

from datetime import datetime

from EventApp.models import *
from EventApp import settings

import json
import urllib

import utils

def event(request, years, months, days):
    event = Event.objects.filter(age_years=years, age_months=months, age_days=days)
    response = serializers.serialize("json", event) 
    return HttpResponse(response)

@csrf_exempt
def test(request):
    print request
    return render_to_response("base.html")

@csrf_exempt
def update_birthday(request, user_id):
    post = request.body
    body_dict = json.loads(post)
    bday = datetime.strptime(body_dict['birthday'], "%Y/%m/%d")

    try:
        user = EventUser.objects.get(facebook_id=user_id)
    except EventUser.DoesNotExist as e:
        user = EventUser(facebook_id=user_id)


    user.birthday = bday
    user.save()

    return HttpResponse(content="User saved")

def create_simple_error(message):

    return "{'error' : '%s'}" % message

def related_events(request, event_id):

    try:

        formatted_cookie = request.COOKIES['AtYourAge'].replace("'", "\"")
        user_dict = json.loads(formatted_cookie)

        access_token = user_dict['token']
        user_id = user_dict['activeUserId']
        requesting_user = EventUser.objects.get(facebook_id=user_id)
        requesting_user.num_requests = requesting_user.num_requests + 1;
        requesting_user.save()


    except KeyError:
        access_token = ""
        user_id = ""

    try:
        the_event = Event.objects.get(id=event_id)
        events = Event.objects.filter(figure=the_event.figure)
    except Event.DoesNotExist:
        return HttpResponse(content=create_simple_error("Could not find related event for event with id %s" % event_id))

  
    event_arr = []

    for event in events:

        description = "%s%s" % (event.description[0].upper(), event.description[1:])

        e_dict = {'description' : description,
                 'age_days' : event.age_days,
                 'age_months' : event.age_months,
                 'age_years' : event.age_years,
                 'is_self' : False,
                 }
        if event.id == int(event_id):
            e_dict['is_self'] = True

        event_arr.append(e_dict)

    ret_val = {'parent_id' : event_id,
               'events' : event_arr
               }
 

    json_string = json.dumps(ret_val)

    return HttpResponse(content=json_string, content_type="application/json")

        
def sample_events(request):

    all_events = Event.objects.all()

    sample_events = sample(all_events, 5)

    response = serialize_event_json(sample_events)

    return HttpResponse(response)


def serialize_event_json(events):

    event_array = []
    for event in events:
     
        description = "%s%s" % (event.description[0].capitalize(), event.description[1:])
        figure_dict = {
                'id' : event.figure.id,
                'name' : event.figure.name,
                'image_url' : event.figure.image_url
                }
        event_dict = {
                'figure' : figure_dict,
                'age_years' : event.age_years,
                'age_months' : event.age_months,
                'age_days' : event.age_days,
                'event_description' : description,
                'event_id' : event.id 
                }
        event_array.append(event_dict)

    retval = json.dumps(event_array)

    return retval


def story_with_birthday(request, fb_id ):

#    import pdb; pdb.set_trace()
    try:

        formatted_cookie = request.COOKIES['AtYourAge'].replace("'", "\"")
        user_dict = json.loads(formatted_cookie)

        access_token = user_dict['token']
        user_id = user_dict['activeUserId']
    except KeyError:
        access_token = ""
        user_id = ""


    try:
        user = EventUser.objects.get(facebook_id=fb_id)

        if user.first_name == None or user.last_name == None or user.birthday == None:
            utils.populate_user_with_fb_fields(user, access_token)
            user.save()

    except EventUser.DoesNotExist:
        user = EventUser(facebook_id=fb_id)
        user.date_added = datetime.now()
        utils.populate_user_with_fb_fields(user, access_token)
        user.save()

    try:
        requesting_user = EventUser.objects.get(facebook_id=user_id)
        requesting_user.date_last_seen = datetime.now()

        if user.id != requesting_user.id:
            user.added_by.add(requesting_user)
            user.save()

        if requesting_user.num_requests != None:
            requesting_user.num_requests = requesting_user.num_requests + 1
        else:
            requesting_user.num_requests = 1

        requesting_user.save()
    except EventUser.DoesNotExist:
        pass
    bday = user.birthday
 
    elapsed_time = utils.get_age(bday.year, bday.month, bday.day)

    years = elapsed_time["years"]
    months = elapsed_time["months"]
    days = elapsed_time["days"]
   

    person_profile_pic = utils.person_profile_pic(fb_id, access_token)
    events = Event.objects.filter(age_years=years, age_months=months, age_days=days)
    event_list = []
    event = events[0]
    event = events[0]
    sex = "he"
 
    if event.male == False:
        sex = "she"
   
    description = "%s%s" % (event.description[0].capitalize(), event.description[1:])

    info_dict = {'person_profile_pic' : person_profile_pic,
            'figure_profile_pic' : event.figure.image_url,
            'figure_id' : event.figure.id,
            'figure_name' : event.figure.name,
            'age_years' : years,
            'age_months' : months,
            'age_days' : days,
            'figure_pronoun' : sex,
            'figure_event' : description,
            'event_id' : event.id }

    response = json.dumps(info_dict)

    return HttpResponse(response)

def figure_info(request, figure_id):

    try:
        figure = Figure.objects.get(id=figure_id)
    except Figure.DoesNotExist:
        return HttpResponse(content=create_simple_error("Figure with id %s does not exist." % figure_id))


#    [figure_dict.__setitem__(key, figure.__getattribute__(key).encode('utf-8')) for key in figure._meta.get_all_field_names() if key != "event"]

    keys = ['name', 'image_url', 'description', 'date_of_birth', 'date_of_death']


    figure_dict = {'name' : figure.name,
            'image_url' : figure.image_url,
            'description' : "",
            'date_of_birth' : "",
            'date_of_death' : "",
    }

    if figure.date_of_birth != None:
        dob = figure.date_of_birth
        if dob.year > 1900:
            figure_dict['date_of_birth'] = dob.strftime("%m/%d/%Y")
        else:
            figure_dict['date_of_birth'] = "%i/%i/%i" % (dob.month, dob.day, dob.year)
    if figure.date_of_death != None:
        dod = figure.date_of_death
        if dod.year > 1900:
            figure_dict['date_of_death'] = dod.strftime("%m/%d/%Y")
        else:
            figure_dict['date_of_death'] = "%i/%i/%i" % (dod.month, dod.day, dod.year)


    if figure.description != None:
        figure_dict['description'] = figure.description.encode('utf-8')


    json_string = json.dumps(figure_dict)

    return HttpResponse(content=json_string)

