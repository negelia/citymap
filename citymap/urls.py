from django.urls import path
from map import views
from map.models import cityObject
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
    path('map/', views.map_view, name='map_view'),
    path('api/markers/', views.get_markers, name='get_markers'),
    path('api/markers/add/', views.add_cityObject, name='add_cityObject'),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)