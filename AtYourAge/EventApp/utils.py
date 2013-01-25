from datetime import datetime
from math import floor
from facebook import facebook

def get_age(year, month, day):


     now = datetime.now()
     birthday = datetime(year, month, day)

     delta = now - birthday
     days_delta = float(delta.days)

     years_old = days_delta / 365.25
     months_old = (years_old * 12) % 12
     months_old_delta = years_old * 12
     days_old = now.day - birthday.day 
     if days_old < 0:
         days_old = abs(days_old)
         days_old = days_old + now.day
     print months_old - floor(months_old)
     print years_old, months_old, days_old
     delta_list = map(int, map(floor, [years_old, months_old, days_old]))

     ddict = {"years": delta_list[0], "months": delta_list[1], "days": delta_list[2]}
     return ddict 

def figure_profile_pic(event_obj, access_token=None):
    graph_obj = facebook.GraphAPI(access_token)
    results = graph_obj.get_object("search", q=event_obj.name, type="page")

    public_figures = [result['id'] for result in results['data'] if result['category'] == "Public figure"]   
              
    ret_dict = {"image_found" : False, "img_url" : ""}
    try:
        first_result_id = public_figures[0]
        img_href = graph_obj.get_object(first_result_id, fields="picture")['picture']['data']['url']
        ret_dict['image_found'] = True
        ret_dict['img_url'] = img_href
    except:
        ret_dict['image_found'] = False

    return ret_dict

def person_profile_pic(id, access_token=None):

    graph = facebook.GraphAPI(access_token)

    fb_object = graph.get_object(id, fields="picture")

    print fb_object

    picture_info = fb_object['picture']['data']

    if picture_info['is_silhouette'] == False:
        return picture_info['url']

