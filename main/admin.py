from django.contrib import admin
from .models import Profile
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "creator", "background_color")
    filter_horizontal = ("subscribers",)

admin.site.register(Profile)
admin.site.register(Event, EventAdmin)