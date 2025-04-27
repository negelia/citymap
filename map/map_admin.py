from django.contrib import admin
from map.models import cityObject
from .map_admin import MapAdmin

@admin.register(cityObject)
class cityObjectAdmin(MapAdmin):
    list_display = ('title', 'lat', 'lng', 'moderated')
    list_editable = ('moderated',)
    list_filter = ('moderated', 'category')