from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required
from .models import cityObject
from .forms import CityObjectModerationForm  # Убедитесь, что этот файл существует
import logging
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

def home(request):
    """Перенаправление на карту"""
    return redirect('map_view')

@login_required
def map_view(request):
    """Отображение карты с объектами"""
    return render(request, 'map/map.html')

def get_markers(request):
    """API для получения маркеров"""
    markers = cityObject.objects.filter(status='approved').values(
        'id', 'title', 'lat', 'lng', 'category', 'photo'
    )
    return JsonResponse(list(markers), safe=False)

@csrf_exempt
@login_required
def add_cityObject(request):
    """API для добавления нового объекта"""
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST method allowed'
        }, status=405)

    try:
        required_fields = ['lng', 'lat', 'title', 'category']
        for field in required_fields:
            if field not in request.POST:
                raise ValidationError(f'Missing required field: {field}')

        marker = cityObject.objects.create(
            lng=float(request.POST['lng']),
            lat=float(request.POST['lat']),
            title=request.POST['title'],
            description=request.POST.get('desc', ''),
            rating=int(request.POST.get('rating', 3)),
            category=request.POST['category'],
            photo=request.FILES.get('photo'),
            created_by=request.user
        )

        logger.info(f"Created marker ID: {marker.id} by user {request.user}")
        return JsonResponse({
            'status': 'success',
            'id': marker.id,
            'moderated': marker.status == 'approved'
        })

    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
        
    except Exception as e:
        logger.error(f"Error creating marker: {str(e)}", exc_info=True)
        return JsonResponse({
            'status': 'error',
            'message': 'Internal server error'
        }, status=500)

# Добавляем недостающие функции для модерации
@permission_required('map.can_moderate_cityobjects')
def moderate_cityobjects(request):
    """Список объектов на модерации"""
    objects = cityObject.objects.filter(status='pending')
    return render(request, 'map/moderate_list.html', {'objects': objects})

@permission_required('map.can_moderate_cityobjects')
def moderate_cityobject_detail(request, object_id):
    """Детальная страница модерации объекта"""
    obj = get_object_or_404(cityObject, id=object_id)
    
    if request.method == 'POST':
        form = CityObjectModerationForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.moderator = request.user
            obj.save()
            return redirect('moderate_cityobjects')
    else:
        form = CityObjectModerationForm(instance=obj)
    
    return render(request, 'map/moderate_detail.html', {
        'object': obj,
        'form': form,
    })