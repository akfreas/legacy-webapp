import os, sys
sys.path.append('/home/ec2-user/apps/AtYourAge/atyourage-django')
import site
site.addsitedir('/home/ec2-user/apps/AtYourAge/lib/python2.7/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'atyourage.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()