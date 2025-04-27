from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import cityObject
from map.models import cityObject  
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging

def home(request):
    return redirect('map_view')

def map_view(request):
    return render(request, 'map/map.html')

def get_markers(request):
    markers = cityObject.objects.all().values(
        'id', 'title', 'lat', 'lng', 'category', 'moderated'
    )
    return JsonResponse(list(markers), safe=False)

logger = logging.getLogger(__name__)

@csrf_exempt
def add_cityObject(request):
    logger.info("Received request to add marker")
    if request.method == 'POST':
        try:
            logger.info(f"POST data: {request.POST}")
            logger.info(f"FILES: {request.FILES}")
            
            # Создаем объект
            marker = cityObject.objects.create(
                lng=float(request.POST.get('lng')),
                lat=float(request.POST.get('lat')),
                title=request.POST.get('title'),
                description=request.POST.get('desc', ''),
                rating=int(request.POST.get('rating', 3)),
                category=request.POST.get('category'),
                moderated=request.POST.get('moderated', 'false').lower() == 'true',
                photo=request.FILES.get('photo')
            )
            
            logger.info(f"Created marker with ID: {marker.id}")
            return JsonResponse({
                'status': 'success',
                'id': marker.id,
                'moderated': marker.moderated
            })
            
        except Exception as e:
            logger.error(f"Error creating marker: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Only POST method allowed'
    }, status=405)