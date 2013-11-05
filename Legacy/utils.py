#!/usr/bin/env python
try:
    from facebook import GraphAPI
except ImportError:
    from facebook.facebook import GraphAPI



from datetime import datetime
from math import floor
import requests
import string
import json
import re
from dateutil import relativedelta
from EventApp.models import *
from hashlib import md5
import os
from PIL import Image

def get_age(year, month, day):


     now = datetime.now()
     birthday = datetime(year, month, day)
     delta = relativedelta.relativedelta(now, birthday)
     ddict = {"years": delta.years, "months": delta.months, "days": delta.days}
     return ddict 

def figure_wikipedia_pic(figure_name, image_height):


    wiki_images_url =  "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=images&redirects" % figure_name
    wiki_images_get = requests.get(wiki_images_url)
    wiki_json = wiki_images_get.json()
    wiki_page_url  = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=content&rvsection=0&redirects" % figure_name
    wiki_page_json = requests.get(wiki_page_url).json()
    try:
        redirect_array = wiki_page_json['query']['redirects']
        redirect_name = redirect_array[0]['to']

        wiki_images_url =  "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=images&redirects" % redirect_name
    #    print "Redirected images url: %s" % wiki_images_url
        wiki_images_get = requests.get(wiki_images_url)
        wiki_json = wiki_images_get.json()

        wiki_page_url  = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=revisions&rvprop=content&rvsection=0&redirects" % redirect_name

    #    print "Redirected page url: %s" % wiki_page_url
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
        image_regex = re.compile(".*(image|image_name)\s*=\s*(?P<imagename>[a-zA-Z0-9\-\._~:/?#\[\]@!$&'()*+,;= ]*\.(?P<image_extension>jpg|png|gif))")
        image_match = image_regex.match(wiki_page_json)
        image_urls = []
        if image_match == None:
            image_urls = []
        else:
            print "Image match: %s" % image_match.groupdict()['imagename']
            match_dict = image_match.groupdict()
            first_image = match_dict['imagename']

            image_url = "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=File:%s&prop=imageinfo&iiprop=url" % first_image
            print "Image url: %s" % image_url
            image_info = requests.get(image_url).json()
            image_query = image_info['query']
            print "Image info: %s" % str(image_info)

            pages = image_query['pages']
            print pages
            for page_key in pages.keys():
                image_info_dict = {}

                if "title" in pages[page_key].keys():
                    raw_image_title = pages[page_key]["title"]
                    image_title = raw_image_title.split(":")[1].replace(" ", "_")

                if "imageinfo" in pages[page_key].keys():
                    imageinfo = pages[page_key]['imageinfo']
                    for info in imageinfo:
                        
                        print info
                        if match_dict['image_extension'] != 'gif':
                            url_split = info['url'].split("commons")
                            url_split.insert(1, "/commons/thumb")
                            formatted_url = "".join(url_split)
                            resized_url = "%s/%dpx-%s" % (formatted_url, image_height, image_title)
                            image_urls.append(info['url'])
                        else:
                            image_urls.append(info['url'])

    except KeyError:
        print "Hit keyerror."
        image_urls = []
    except TypeError:
        print "Hit typeerror."
        image_urls = []

    print image_urls

    if len(image_urls) > 0:
        return image_urls[0]

def figure_freebase_pic(figure_name, image_height):

    formatted_name = figure_name.lower().replace(" ", "_")
    api_key = "AIzaSyDN15Pi0PJpqnNlM64xiE65yW9shiZ2A1I"
    url = "https://www.googleapis.com/freebase/v1/topic/en/%s?key=%s&filter/common/topic/image&limit=1" % (formatted_name, api_key)
    
#    import pdb;pdb.set_trace()

    img_request = requests.get(url).json()
    if "error" not in img_request.keys():
        img_id = img_request['id']
        url = "https://usercontent.googleapis.com/freebase/v1/image%s?maxwidth=%s&key=%s" % (img_id, image_height, api_key)
        return url
    else:
        return None


def populate_figure_datapoints(figure):

    formatted_name = figure.name.lower().replace(" ", "_")
    api_key = "AIzaSyDN15Pi0PJpqnNlM64xiE65yW9shiZ2A1I"
    url = "https://www.googleapis.com/freebase/v1/topic/en/%s?key=%s&limit=1" % (formatted_name, api_key)

    try:
        full_json = requests.get(url).json()['property']
    except KeyError:
        return

    try:
        print full_json.keys()

        dob_parse = lambda x: x['values'][0]['text']
        dod_parse =  dob_parse
        desc_parse = lambda x: x['values'][0]['value']

        parsers = {'/common/topic/description' : desc_parse,
                '/people/person/date_of_birth'  : dob_parse,
                '/people/deceased_person/date_of_death' : dod_parse}

        keymap = {'/common/topic/description' : 'description', 
                '/people/person/date_of_birth' : 'date_of_birth', 
                '/people/deceased_person/date_of_death' : 'date_of_death'} 

        keys = keymap.keys()

        available_keys = [key for key in full_json.keys() if key in keys]

        for k in available_keys:
            property_name = keymap[k]
            parser = parsers[k]
            print full_json[k]
            figure.__setattr__(property_name, parser(full_json[k]))

        figure.save()
    except:
        print "Could not populate record for %s." % figure.name


        

def figure_fb_profile_pic(figure_name, image_height):
    graph_obj = GraphAPI()
    results = graph_obj.get_object("search", q=figure_name, type="page")

    public_figures = [result['id'] for result in results['data'] if result['category'] == "Public figure"]   
              
    try:
        first_result_id = public_figures[0]
        img_href = "https://graph.facebook.com/%s/picture?height=%s" % (first_result_id, image_height)
    except:
        return None

    return img_href

def figure_pic_href(name, size):

    fetch_functions = [figure_freebase_pic, figure_wikipedia_pic]
    image_url = None


    while len(fetch_functions) > 0 and (image_url == None or len(image_url) < 0):

        function = fetch_functions.pop()
        image_url = function(name, size)
        
    return image_url


def import_data_to_s3(num_import):

    content_map = {'image/jpeg' : 'jpg', 'image/png' : 'png', 'image/jpg' : 'jpg', 'image/gif' : 'gif'}

    from boto.s3.connection import S3Connection
    from boto.s3.key import Key
    from tempfile import mkdtemp
    
    conn = S3Connection(aws_access_key_id="AKIAIQBQCAWC6FTCPFRQ", aws_secret_access_key="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")
    bucket = conn.get_bucket("legacyapp-images")

    figures = Figure.objects.all()
    
    temp_dir = mkdtemp()
    

    counter = 0;

    for figure in figures:

        pic_url = figure_pic_href(figure.name, 200)
            
        print figure

        if pic_url != None:

            print "Pulling from %s." % pic_url

            pic_hash = md5(pic_url).hexdigest()
            pic_request = requests.get(pic_url, verify=False)
            pic_file_extension = pic_url.split(".")[-1]
            content_type = pic_request.headers['content-type']

            if "image" in content_type:

                pic_filename = temp_dir + "/" + pic_hash
                pic_fp = open(pic_filename, "w")
                pic_fp.write(pic_request.content)
                pic_fp.close()
                image_file_size = os.path.getsize(pic_filename)

                if  image_file_size > 10**5:
                    
                    image = Image.open(pic_filename)

                    new_size = map(lambda x: 200*x/(image_file_size/1000), image.size)

                    print "Resizing to %s" % new_size

                    try:

                        new_image = image.resize(new_size)
                        new_image.save("%s.%s" % (pic_filename, content_map[content_type]))
                    except IOError:

                        figure.image_url = "not_found_0"
                        figure.save()
                        break

                    pic_filename += "." + content_map[content_type]

                pic_fp = open(pic_filename, "r")

                s3_pic_key = Key(bucket)

                s3_pic_key.set_contents_from_file(pic_fp)
                s3_pic_key.set_acl("public-read")

                s3_pic_url = "http://%s.s3.amazonaws.com/%s" % (bucket.name, s3_pic_key.md5)

                figure.image_url = s3_pic_url
                figure.save()
                counter += 1

            else:
                figure.image_url = "not_found_1"
                figure.save()

        else:
            figure.image_url = "not_found_2"
            figure.save()



    print "%d events out of %d updated with url." % (counter, num_import)

         
def import_until_done():
    
    figures_nopic = Figure.objects.filter(image_url="not_found")


    while figures_nopic.count() > 100:

        #import pdb; pdb.set_trace()
        import_data_to_s3(100)
        figures_nopic = Figure.objects.filter(image_url="not_found")



def person_profile_pic(id, access_token=None):

    graph = GraphAPI(access_token)

    fb_object = graph.get_object(id, fields="picture")

    picture_info = fb_object['picture']['data']

    if picture_info['is_silhouette'] == False:
        return picture_info['url']



def populate_user_with_fb_fields(user,  access_token):

    graph = GraphAPI(access_token)
    fb_object = graph.get_object(user.facebook_id, fields="first_name,last_name,birthday")
    print fb_object

    try:
        user.first_name = fb_object['first_name']
        user.last_name = fb_object['last_name']
        try:
            user.birthday = datetime.strptime(fb_object['birthday'], "%m/%d/%Y")
        except ValueError:
            print "User birthday not found: %s" % fb_object
            user.birthday = None

    except KeyError as e:
        print "User birthday not found: %s" % fb_object
        print e.message

if __name__ == '__main__':

    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EventApp.settings")

    import_until_done()
