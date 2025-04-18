from django.shortcuts import render, redirect
from .models import cityObject
from .forms import cityObjectForm, ObjectFilterForm  
from django.conf import settings

def map_view(request):
    objects = cityObject.objects.filter(approved=True)
    
    filter_form = ObjectFilterForm(request.GET)
    if filter_form.is_valid():
        object_type = filter_form.cleaned_data.get('object_type')
        if object_type:
            objects = objects.filter(object_type=object_type)
    
    context = {
        'objects': objects,
        'MAPBOX_KEY': settings.MAPBOX_KEY,
        'filter_form': filter_form,  
    }
    return render(request, 'map/map.html', context)

def add_cityObject(request):
    if request.method == 'POST':
        form = cityObjectForm(request.POST)
        if form.is_valid():
            city_object = form.save(commit=False)  
            city_object.approved = True  
            city_object.save()  
            return redirect('map_view')
    else:
        form = cityObjectForm()
    return render(request, 'add.html', {'form': form})

def home(request):
    return redirect('map_view')  