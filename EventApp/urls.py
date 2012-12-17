from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('EventApp.views',

     url(r'^admin/', include(admin.site.urls)),
     url(r'^event/elapsed/(\d{1,2})/(\d{1,2})/(\d{1,2})', 'event'), 
     url(r'^event/(\d{4})/(\d{1,2})/(\d{1,2})', 'event_with_birthday') 
)
