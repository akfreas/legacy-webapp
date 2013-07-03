from django.template import RequestContext, loader
from django.http.response import *
from django.shortcuts import render_to_response
from django.core import serializers
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from ios_notifications.models import Device as DV, APNService

from random import sample

from datetime import datetime

from EventApp.models import *
from EventApp import settings

import json
import urllib

import utils

min_events = 5

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

@csrf_exempt
def add_users(request):
    post = request.body
    person_array = json.loads(post)

    formatted_cookie = request.COOKIES['AtYourAge'].replace("'", "\"")
    user_dict = json.loads(formatted_cookie)

    access_token = user_dict['token']
    user_id = user_dict['activeUserId']


    requesting_user = get_or_create_user(user_id, access_token)

    for fb_id in person_array:

        
        try:
            fb_user = EventUser.objects.get(facebook_id=fb_id)
            
        except EventUser.DoesNotExist as e:
            fb_user = EventUser(facebook_id=fb_id)
            utils.populate_user_with_fb_fields(fb_user, access_token)
            fb_user.save()

        fb_user.added_by.add(requesting_user)

    return HttpResponse(content="%s users saved/updated." % len(person_array))

@csrf_exempt
def save_device_information(request):

    access_token, user_id = info_from_request_cookie(request)

    post_data = json.loads(request.body)

    device = get_or_create_device(post_data['device_token'])
    device.last_seen = datetime.now()

    if access_token != None and user_id != None:

        user = get_or_create_user(user_id, access_token)
        if user not in device.associated_with.all():
            device.associated_with.add(user)

    device.save()

    return HttpResponse("{'message' : 'ok'}")

         


def create_simple_error(message):

    return "{'error' : '%s'}" % message

def get_or_create_device(device_token):
    
    try:
        device = Device.objects.get(device_token=device_token)

    except Device.DoesNotExist:
        device = Device(device_token=device_token)

    apn_service = APNService.objects.get(name='legacyapp')
    apn_device = DV(token=device_token, service=apn_service)
    apn_device.save()
    return device

def get_or_create_user(facebook_id, access_token):

    try:
        user = EventUser.objects.get(facebook_id=facebook_id)

    except EventUser.DoesNotExist:
        user = EventUser(facebook_id=facebook_id)
        user.date_added = datetime.now()
        utils.populate_user_with_fb_fields(user, access_token)
        user.save()

    return user

def related_events(request, event_id):

    try:

        formatted_cookie = request.COOKIES['AtYourAge'].replace("'", "\"")
        user_dict = json.loads(formatted_cookie)

        access_token = user_dict['token']
        user_id = user_dict['activeUserId']
        requesting_user = EventUser.objects.get(facebook_id=user_id)
        if requesting_user.num_requests == None:
            requesting_user.num_requests = 1;
        else:
            requesting_user.num_requests = requesting_user.num_requests + 1;
        requesting_user.save()

    except EventUser.DoesNotExist:
        new_user = EventUser(facebook_id=user_id)
        new_user.num_requests = 0
        user.date_added = datetime.now()
        utils.populate_user_with_fb_fields(new_user, access_token)
        new_user.save()


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

def events_for_figure(request, figure_id):

    events = Event.objects.filter(figure__id=figure_id)
    if events.count() < 1:
        return HttpResponse(content=create_simple_error("no events found for figure %s" % figure_id))

 
    event_array = serialize_event_json_array(events)

    event_json = json.dumps(event_array)

    return HttpResponse(content=event_json, content_type="application/json")
    

def info_from_request_cookie(request):
    try:
        formatted_cookie = request.COOKIES['AtYourAge'].replace("'", "\"")
        user_dict = json.loads(formatted_cookie)

        access_token = user_dict['token']
        user_id = user_dict['activeUserId']

    except KeyError:
        access_token = None
        user_id = None

    return access_token, user_id

        
def sample_events(request):

    all_events = Event.objects.all().exclude(figure__image_url="not_found")

    sample_events = sample(all_events, 5)

    response_array = serialize_event_json_array(sample_events)

    response = json.dumps(response_array)
    return HttpResponse(response)


def events(request):

    access_token, user_id = info_from_request_cookie(request)

    if access_token == None or user_id == None:

        all_events = Event.objects.all().exclude(figure__image_url="not_found")

        sample_events = sample(all_events, 5)

        response_array = serialize_event_json_array(sample_events)

        response = json.dumps(response_array)
        return HttpResponse(response, content_type="application/json")


    requesting_user = get_or_create_user(user_id, access_token)

    user_friends = EventUser.added_by.through.objects.filter(to_eventuser=requesting_user) 

    all_users = user_friends

    event_array = []

    def event_dict_for_user(user):
        age = utils.get_age(user.birthday.year, user.birthday.month, user.birthday.day)
        event = Event.objects.filter(age_years=age['years'], age_months=age['months'], age_days=age['days'])
        if event.count() > 0:
            event_dict = serialize_event_json(event[0])
            
            user_dict = serialize_eventuser_json(user, access_token)

            event_dict['person'] = user_dict
            return event_dict


    for user_addedby in all_users:
            user = user_addedby.from_eventuser
            if user.birthday != None:
                event_dict = event_dict_for_user(user)
                if event_dict != None:
                    event_array.append(event_dict)

    event_array.append(event_dict_for_user(requesting_user))

    all_events = Event.objects.all().exclude(figure__image_url="not_found")
    num_all_events = len(event_array)

    if num_all_events < min_events:
        sample_events = sample(all_events, min_events - num_all_events)
        event_array += serialize_event_json_array(sample_events)




    print event_array
    json_dict = json.dumps(event_array)

    return HttpResponse(content=json_dict, content_type="application/json")


   

def serialize_eventuser_json(person, access_token):

    profile_pic = utils.person_profile_pic(person.facebook_id, access_token)

    user_dict = {
            'facebook_id' : person.facebook_id,
            'first_name' : person.first_name,
            'last_name' : person.last_name,
            'birthday' : person.birthday.strftime("%m/%d/%Y"),

            'profile_pic' : profile_pic
            }
    return user_dict

def serialize_event_json_array(events):

    event_array = []
    for event in events:
        event_dict = serialize_event_json(event)
        event_array.append(event_dict)


    return event_array

def serialize_event_json(event): 

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
        
        return event_dict

def story_with_birthday(request, fb_id ):

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

