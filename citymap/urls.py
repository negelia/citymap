from django.contrib import admin
from django.urls import path
from map import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('map/', views.map_view, name='map_view'),  
    path('add/', views.add_cityObject, name='add_cityObject'),  
]