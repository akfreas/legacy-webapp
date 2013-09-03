from django.contrib import admin
from EventApp.models import *


class EventAdmin(admin.ModelAdmin):

    list_display = ("figure", "description", "age_years", "age_months", "age_days", "male")
    list_filter = ("male",)

admin.site.register(Event, EventAdmin)

class FigureAdmin(admin.ModelAdmin):

    def profile_pic(self, obj):
        return "<img src='%s' height='100'>" % obj.image_url

    search_fields = ["name"]
    profile_pic.allow_tags = True
    list_display = ("name", "image_url", "profile_pic", "date_of_birth", "date_of_death")

admin.site.register(Figure, FigureAdmin)

class EventUserAdmin(admin.ModelAdmin):

    list_display = ("facebook_id", "first_name", "last_name", "date_first_seen", "date_last_seen", "date_added", "num_requests")
    pass

admin.site.register(EventUser, EventUserAdmin)

class DeviceAdmin(admin.ModelAdmin):

    list_display = ("device_token", "date_added", "date_last_seen",)

admin.site.register(Device, DeviceAdmin)
