from datetime import datetime
from math import floor
from facebook import facebook
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

        

def figure_fb_profile_pic(figure_name, image_height):
    graph_obj = facebook.GraphAPI()
    results = graph_obj.get_object("search", q=figure_name, type="page")
    print results

    public_figures = [result['id'] for result in results['data'] if result['category'] == "Public figure"]   
    print public_figures
              
    try:
        first_result_id = public_figures[0]
        img_href = "https://graph.facebook.com/%s/picture?height=%s" % (first_result_id, image_height)
        print "Href: %s" % img_href
    except:
        return None

    return img_href

def figure_pic_href(name, size):

    fetch_functions = [figure_wikipedia_pic, figure_fb_profile_pic]
    image_url = None

    print "Finding picture for %s" % name

    while len(fetch_functions) > 0 and (image_url == None or len(image_url) < 0):

        function = fetch_functions.pop()
        image_url = function(name, size)
        
    print "Found %s" % image_url
    return image_url


def import_data_to_s3(num_import):

    content_map = {'image/jpeg' : 'jpg', 'image/png' : 'png', 'image/jpg' : 'jpg'}

    from boto.s3.connection import S3Connection
    from boto.s3.key import Key
    from tempfile import mkdtemp
    
    conn = S3Connection(aws_access_key_id="AKIAIS5NHCFOO3QE6GNQ", aws_secret_access_key="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")
    bucket = conn.get_bucket("atyourage-images")

    events = Event.objects.filter(image_url="")[:num_import]
    
    temp_dir = mkdtemp()
    

    counter = 0;

    for event in events:

        pic_url = figure_pic_href(event.name, 200)

        if pic_url != None:

            print "Pulling from %s." % pic_url

            pic_hash = md5(pic_url).hexdigest()
            pic_request = requests.get(pic_url)
            

            if "image" in pic_request.headers['content-type']:

                pic_filename = temp_dir + "/" + pic_hash
                pic_fp = open(pic_filename, "w")
                pic_fp.write(pic_request.content)
                pic_fp.close()
                image_file_size = os.path.getsize(pic_filename)

                if  image_file_size > 10**5:
                    
                    image = Image.open(pic_filename)

                    new_size = map(lambda x: 200*x/(image_file_size/1000), image.size)

                    print "Resizing to %s" % new_size

                    new_image = image.resize(new_size)
                    pic_filename += ".jpg"
                    new_image.save(pic_filename)

                pic_fp = open(pic_filename, "r")

                s3_pic_key = Key(bucket)

                s3_pic_key.set_contents_from_file(pic_fp)
                s3_pic_key.set_acl("public-read")

                s3_pic_url = "http://%s.s3.amazonaws.com/%s" % (bucket.name, s3_pic_key.md5)

                event.image_url = s3_pic_url
                event.save()

                counter += 1



    print "%d events out of %d updated with url." % (counter, num_import)

         

            








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
