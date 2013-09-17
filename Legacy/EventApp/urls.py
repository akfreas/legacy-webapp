from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('EventApp.views',

     url(r'^admin/', include(admin.site.urls)),
     url(r'^$', 'test'),

     url(r'^events', 'events'),
     url(r'^figure/(\d*)/events', 'events_for_figure'),

     url(r'^users/add', 'add_users'),
     url(r'^user/(\d*)/update_birthday', 'update_birthday'),
     url(r'^device/information', 'save_device_information'),
     url(r'^ios-notifications/', include('ios_notifications.urls')),

)