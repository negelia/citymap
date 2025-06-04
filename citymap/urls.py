from django.urls import path
from django.urls import include
from django.contrib import admin
from map.views import (
    home,
    map_view,
    get_markers,
    add_cityObject,
    moderate_cityobjects,
    moderate_cityobject_detail
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('moderate/', moderate_cityobjects, name='moderate_cityobjects'),
    path('moderate/<int:object_id>/', moderate_cityobject_detail, name='moderate_cityobject_detail'),
    path('', home, name='home'),
    path('map/', map_view, name='map_view'),
    path('api/markers/', get_markers, name='get_markers'),
    path('api/markers/add/', add_cityObject, name='add_cityObject'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]