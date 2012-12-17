from django.contrib import admin
from EventApp.models import *

class EventAdmin(admin.ModelAdmin):

    list_display = ("name", "description", "age_years", "age_months", "age_days", "male")
    list_filter = ("male",)


admin.site.register(Event, EventAdmin)
