from django.contrib import admin
from .models import cityObject
from mapbox_location_field.admin import MapAdmin

@admin.register(cityObject)
class cityObjectAdmin(MapAdmin):
    list_display = ('name', 'lat', 'lon', 'approved')
    list_editable = ('approved',)
    list_filter = ('approved',)