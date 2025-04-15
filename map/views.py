from django.shortcuts import render, redirect
from .models import cityObject
from .forms import cityObjectForm
from django.conf import settings

def map_view(request):
    objects = cityObject.objects.filter(approved=True)  
    context = {
        'objects': objects,
        'MAPBOX_KEY': settings.MAPBOX_KEY
    }
    return render(request, 'map/map.html', context)

def add_cityObject(request):
    if request.method == 'POST':
        form = cityObjectForm(request.POST)
        if form.is_valid():
            city_object = form.save(commit=False)  # Сохраняем объект, но не сохраняем в БД ещё
            city_object.approved = True  # Устанавливаем approved в True
            city_object.save()  # Теперь сохраняем в БД
            return redirect('map_view')
    else:
        form = cityObjectForm()
    return render(request, 'add.html', {'form': form})

def home(request):
    return redirect('map_view')  