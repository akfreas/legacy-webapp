from datetime import datetime
from math import floor
from facebook import facebook
import requests
import string
import json
import re
from dateutil import relativedelta

def get_age(year, month, day):


     now = datetime.now()
     birthday = datetime(year, month, day)
     delta = relativedelta.relativedelta(now, birthday)
     ddict = {"years": delta.years, "months": delta.months, "days": delta.days}
     return ddict 

def figure_wikipedia_pic(figure_name, image_size):


    wiki_images_url =  "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=images&redirects" % figure_name
    print wiki_images_url
    wiki_images_get = requests.get(wiki_images_url)
    wiki_json = wiki_images_get.json()
    wiki_page_url  = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=content&rvsection=0&redirects" % figure_name
    print wiki_page_url
    wiki_page_json = requests.get(wiki_page_url).json()
    try:
        redirect_array = wiki_page_json['query']['redirects']
        redirect_name = redirect_array[0]['to']

        wiki_images_url =  "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=images&redirects" % redirect_name
        print "Redirected images url: %s" % wiki_images_url
        wiki_images_get = requests.get(wiki_images_url)
        wiki_json = wiki_images_get.json()

        wiki_page_url  = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=content&rvsection=0&redirects" % redirect_name

        print "Redirected page url: %s" % wiki_page_url
        wiki_page_json = requests.get(wiki_page_url).json()
    except KeyError:
        pass

    wiki_page_json = str(wiki_page_json)

    allowed_extensions = ['jpg', 'png']

    pages = wiki_json['query']['pages']
#    import pdb; pdb.set_trace()
    try:
        """
        images = [pages[key] for key in pages.keys()][0]['images'] #flatten list, this might not work
        print "Images: %s" % images
        first_image = None
        if len(images) > 0:
            for image_dict in images:
                formatted_image_name = image_dict['title'].split(":")[1]
                extension = formatted_image_name.split(".")[-1]
                if re.search(formatted_image_name, wiki_page_json, re.IGNORECASE) != None:
                    first_image = image_dict
        if first_image == None:
            image_files = [image for image in images if image_dict['title'].split(".")[-1] in allowed_extensions]
            if len(image_files) > 0:
                first_image = image_files[0]

        image_urls = []
#    import pdb; pdb.set_trace()
        """
        image_regex = re.compile(".*image\s*=\s*([a-zA-Z0-9\-\._~:/?#\[\]@!$&'()*+,;= ]*\.jpg|png)")
        image_match = image_regex.match(wiki_page_json)
        image_urls = []
        if image_match == None:
            image_urls = []
        else:
            print "Image match: %s" % image_match.groups()[0]
            first_image = image_match.groups()[0]
            image_url = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=File:%s&prop=imageinfo&iiprop=url" % first_image
            print "Image url: %s" % image_url
            image_info = requests.get(image_url).json()
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
        print "Hit keyerror."
        image_urls = []
    except TypeError:
        print "Hit typeerror."
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

#    print fb_object

    picture_info = fb_object['picture']['data']

    if picture_info['is_silhouette'] == False:
        return picture_info['url']

def populate_user_with_fb_fields(user,  access_token):

    graph = facebook.GraphAPI(access_token)
    fb_object = graph.get_object(user.facebook_id, fields="first_name,last_name")
    print fb_object

    try:
        user.first_name = fb_object['first_name']
        user.last_name = fb_object['last_name']
    except KeyError:
        pass
