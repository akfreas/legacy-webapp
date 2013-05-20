from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('EventApp.views',

     url(r'^admin/', include(admin.site.urls)),
     url(r'^$', 'test'),
     url(r'^(\d*)/event/elapsed/(\d{1,2})/(\d{1,2})/(\d{1,2})', 'event'), 
     url(r'^user/(\d*)/story', 'story_with_birthday'),

     url(r'event/(\d*)/related', 'related_events'),
     url(r'figure/(\d*)$', 'figure_info'),

     url(r'^user/(\d*)/update_birthday', 'update_birthday'),
)
