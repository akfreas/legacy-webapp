from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('atyourage.views',
    # Examples:
    # url(r'^$', 'atyourage.views.home', name='home'),
    # url(r'^atyourage/', include('atyourage.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^event/elapsed/(\d{1,2})/(\d{1,2})/(\d{1,2})', 'event'), 
     url(r'^event/(\d{1,2})/(\d{1,2})/(\d{4})', 'event_with_birthday') 
)
