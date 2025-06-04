from django.contrib import admin
from map.models import cityObject
from .map_admin import MapAdmin

@admin.register(cityObject)
class cityObjectAdmin(MapAdmin):
    list_display = ('title', 'lat', 'lng', 'moderated')
    list_editable = ('moderated',)
    list_filter = ('moderated', 'category')
    actions = ['approve_points', 'reject_points']
    
    def approve_points(self, request, queryset):
        queryset.update(status='approved', moderator=request.user)
    approve_points.short_description = "Одобрить выбранные точки"
    
    def reject_points(self, request, queryset):
        queryset.update(status='rejected', moderator=request.user)
    reject_points.short_description = "Отклонить выбранные точки"