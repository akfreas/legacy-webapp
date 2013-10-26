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

min_events = 25

def event(request, years, months, days):
    event = Event.objects.filter(age_years=years, age_months=months, age_days=days)
    response = serializers.serialize("json", event) 
    return HttpResponse(response)

@csrf_exempt
def test(request):
    return HttpResponse(content="Healthy.")

@csrf_exempt
def update_birthday(request, user_id):
    post = request.body
    body_dict = json.loads(post)
    bday = datetime.strptime(body_dict['birthday'], "%Y/%m/%d")

    access_token, requesting_user_id = info_from_request_cookie(request)
    requesting_user = get_or_create_user(requesting_user_id, access_token)
    requesting_user.date_last_seen = datetime.now()
    requesting_user.save()

    user = get_or_create_user(requesting_user_id, access_token)

    user.birthday = bday
    user.save()
    user.added_by.add(requesting_user)
    user.save()
    json_string = json.dumps({'user' : user.facebook_id, 'birthday_saved' : True})

    return HttpResponse(content=json_string, content_type="application/json")

@csrf_exempt
def add_users(request):
    post = request.body
    person_array = json.loads(post)

    access_token, user_id = info_from_request_cookie(request)
    requesting_user = get_or_create_user(user_id, access_token)
    requesting_user.date_last_seen = datetime.now()
    requesting_user.save()

    for person_info in person_array:

        fb_id = person_info['facebook_id']
   
        birthday = datetime.strptime(person_info['birthday'], "%Y/%m/%d")


        fb_user = get_or_create_user(fb_id, access_token)
        fb_user.birthday = birthday
        fb_user.save()
        fb_user.added_by.add(requesting_user)


    json_string = json.dumps({'users_saved' : '%s' % len(person_array)})

    return HttpResponse(content=json_string, content_type="application/json")

def validate_passcode(request, passcode):
    
    print passcode
    dic = {}
    try:
        approved = ApprovedBetaTesters.objects.get(code=passcode)

        dic['verification_status'] = "success"
        dic['message'] = approved.message
        approved.used = True
        approved.time_used = datetime.now()
        approved.save()

    except ApprovedBetaTesters.DoesNotExist:

        dic['verification_status'] = "failure"
        dic['message'] = "Your passcode is invalid.  Sorry!"

    return HttpResponse(content=json.dumps(dic), content_type="application/json")


def delete_user(request, user):

    print request
    access_token, user_id = info_from_request_cookie(request)
    print access_token, user_id
    requesting_user = get_or_create_user(user_id, access_token)
    requesting_user.date_last_seen = datetime.now()
    requesting_user.save()


    user_to_delete = EventUser.objects.get(facebook_id=user)
    user_to_delete.added_by.remove(requesting_user)
    user_to_delete.save()

    json_string = json.dumps({'deleted' : user_to_delete.facebook_id})

    return HttpResponse(content=json_string, content_type="application/json")



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

def events_for_figure(request, figure_id):

    events = Event.objects.filter(figure__id=figure_id)
    if events.count() < 1:
        return HttpResponse(content=create_simple_error("no events found for figure %s" % figure_id))

 
    event_array = serialize_event_json_array(events)

    event_json = json.dumps(event_array)

    return HttpResponse(content=event_json, content_type="application/json")
    

def info_from_request_cookie(request):
    try:
        formatted_cookie = request.COOKIES['LegacyApp'].replace("'", "\"")
        user_dict = json.loads(formatted_cookie)

        access_token = user_dict['token']
        user_id = user_dict['activeUserId']

    except KeyError:
        access_token = None
        user_id = None

    return access_token, user_id

        

def events_for_no_user(request):

    all_events = Event.objects.all().exclude(figure__image_url="not_found")

    sample_events = sample(all_events, min_events)

    response_array = serialize_event_json_array(sample_events)

    response = json.dumps(response_array)
    return HttpResponse(response, content_type="application/json")


def events(request):

    access_token, user_id = info_from_request_cookie(request)

    if access_token == None or user_id == None:
        return events_for_no_user(request)

    requesting_user = get_or_create_user(user_id, access_token)
    requesting_user.date_last_seen = datetime.now()
    requesting_user.save()
    user_friends = EventUser.added_by.through.objects.filter(to_eventuser=requesting_user) 

    all_users = user_friends

    event_array = []

    def event_dict_for_user(user):
        age = utils.get_age(user.birthday.year, user.birthday.month, user.birthday.day)
        event = Event.objects.filter(age_years=age['years'], age_months=age['months'], age_days=age['days'])
        user_dict = serialize_eventuser_json(user, access_token)

        event_dict = {}

        if event.count() > 0:
            event_dict = serialize_event_json(event[0])
            
        else:
            event_dict['error'] = {'NoEventError' : "There are no entries for %s at their age." % user.first_name}

        event_dict['person'] = user_dict

        return event_dict



    for user_addedby in all_users:
            user = user_addedby.from_eventuser
            if user.birthday != None:
                event_dict = event_dict_for_user(user)
                if event_dict != None:
                    event_array.append(event_dict)

    event_array.append(event_dict_for_user(requesting_user))

    all_events = Event.objects.all()
    num_all_events = len(event_array)

    if num_all_events < min_events:
        sample_events = sample(all_events, min_events - num_all_events)
        event_array += serialize_event_json_array(sample_events)




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

