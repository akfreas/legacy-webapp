from django.contrib import admin
from EventApp.models import *
from facebook import facebook


class EventAdmin(admin.ModelAdmin):

    def profile_pic(self, obj):
        graph_obj = facebook.GraphAPI()
        results = graph_obj.get_object("search", q=obj.name, type="page")

        public_figures = [result['id'] for result in results['data'] if result['category'] == "Public figure"]   
                  
        try:
            first_result_id = public_figures[0]
            img_href = graph_obj.get_object(first_result_id, fields="picture")['picture']['data']['url']

            return "<img src='%s'>" % img_href
        except IndexError:
            return "<img src=''>"

    profile_pic.allow_tags = True

    list_display = ("name", "description", "age_years", "age_months", "age_days", "male", "image_url")
    list_filter = ("male",)
    readonly_fields = ("profile_pic",)

class EventUserAdmin(admin.ModelAdmin):

    list_display = ("facebook_id", "first_name", "last_name", "date_first_seen", "date_last_seen", "num_requests")
    pass

admin.site.register(EventUser, EventUserAdmin)

admin.site.register(Event, EventAdmin)
