from django import forms
from .models import cityObject
from map.models import cityObject  

class cityObjectForm(forms.ModelForm):
    class Meta:
        model = cityObject
        fields = ['title', 'lat', 'lng', 'category', 'description', 'rating', 'photo', 'moderated']

class ObjectFilterForm(forms.Form):
    OBJECT_TYPES = [
        ('', 'Все типы'),
        ('toilet', 'Санузел'),
        ('water_refill', 'Пополнение воды'),
        ('rest_area', 'Зона отдыха'),
    ]
    
    object_type = forms.ChoiceField(
        choices=OBJECT_TYPES,
        required=False,
        label="Тип объекта"
    )