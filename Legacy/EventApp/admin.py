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

class ApprovedBetaTesterAdmin(admin.ModelAdmin):

    list_display = ('code', 'name', 'used', 'time_used')
    verbose_name = "Approved Beta Tester"

admin.site.register(ApprovedBetaTesters, ApprovedBetaTesterAdmin)


class EventUserAdmin(admin.ModelAdmin):

    def remove_added_by(modeladmin, request, queryset):

        if request.GET['q'] is not None:

            first_name, last_name = request.GET['q'].split(" ")
            our_user = EventUser.objects.get(first_name__iexact=first_name, last_name__iexact=last_name)

            filtered_objects = EventUser.objects.filter(added_by=our_user)

            for obj in filtered_objects:
                obj.added_by.remove(our_user)
                obj.save()



    list_display = ("facebook_id", "first_name", "last_name", "date_first_seen", "date_last_seen", "date_added", "num_requests")
    search_fields = ('added_by__first_name', 'added_by__last_name')
    actions = ['remove_added_by']

    def get_search_results(self, request, queryset, search_term):

        first_name, last_name = search_term.split(" ")

        our_user = EventUser.objects.get(first_name=first_name, last_name=last_name)

        queryset = EventUser.objects.filter(added_by=our_user)
        
        return queryset, False

    def get_actions(self, request):

        actions = super(EventUserAdmin, self).get_actions(request)
        names = None
        if 'q' in request.GET.keys():
            names = request.GET['q'].split(" ")

        if (names == None):
            del actions['remove_added_by']
        else:
            first_name, last_name = names
            our_user = EventUser.objects.get(first_name__iexact=first_name, last_name__iexact=last_name)
            actions['remove_added_by'] = actions['remove_added_by'][0:2] + ("Remove users added by %s %s" % (first_name, last_name),)

        return actions

admin.site.register(EventUser, EventUserAdmin)

class DeviceAdmin(admin.ModelAdmin):


    def associated_with_formatted(self, obj):
        return ", ".join(["%s %s" % (x.first_name, x.last_name) for x in obj.associated_with.all()])

    associated_with_formatted.short_description = "Associated with user"
    list_display = ("device_token", "date_added", "date_last_seen", "associated_with_formatted")

admin.site.register(Device, DeviceAdmin)
