from datetime import datetime
from math import floor
from facebook import facebook
import requests
import string
import json

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

def figure_wikipedia_pic(figure_name, image_size):


    wiki_images_get = requests.get("http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=images" % figure_name)
    wiki_json = wiki_images_get.json()

    wiki_page_json = requests.get("http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=content&rvsection=0" % figure_name).json()
    wiki_page_json = str(wiki_page_json)

    allowed_extensions = ['jpg', 'png']

    pages = wiki_json['query']['pages']
#    import pdb; pdb.set_trace()
    try:
        images = [pages[key] for key in pages.keys()][0]['images'] #flatten list, this might not work
        first_image = None
        if len(images) > 0:
            for image_dict in images:
                formatted_image_name = image_dict['title'].split(":")[1]
                extension = formatted_image_name.split(".")[-1]
                if string.find(wiki_page_json, formatted_image_name) > -1:
                    first_image = image_dict
        if first_image == None:
            image_files = [image for image in images if image_dict['title'].split(".")[-1] in allowed_extensions]
            if len(image_files) > 0:
                first_image = image_files[0]

        print "FIRST IMAGE: %s"  % first_image
        image_urls = []
#    import pdb; pdb.set_trace()
        image_info = requests.get("http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=imageinfo&iiprop=url" % first_image['title']).json()
        image_query = image_info['query']

        pages = image_query['pages']
        for page_key in pages.keys():
            image_info_dict = {}

            if "title" in pages[page_key].keys():
                raw_image_title = pages[page_key]["title"]
                image_title = raw_image_title.split(":")[1].replace(" ", "_")

            if "imageinfo" in pages[page_key].keys():
                imageinfo = pages[page_key]['imageinfo']
                for info in imageinfo:
                    info['url']
                    url_split = info['url'].split("commons")
                    url_split.insert(1, "commons/thumb")
                    formatted_url = "".join(url_split)
                    resized_url = "%s/%dpx-%s" % (formatted_url, image_size, image_title)
                    image_urls.append({'url' : resized_url, 'title' : image_title})
    except KeyError:
        image_urls = []
    return image_urls
        

def figure_profile_pic(event_obj, access_token=None):
    graph_obj = facebook.GraphAPI(access_token)
    results = graph_obj.get_object("search", q=event_obj.name, type="page")

    public_figures = [result['id'] for result in results['data'] if result['category'] == "Public figure"]   
              
    ret_dict = {"image_found" : False, "url" : ""}
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

