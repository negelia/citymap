from django import forms
from .models import cityObject

class cityObjectForm(forms.ModelForm):
    class Meta:
        model = cityObject
        fields = ['title', 'lat', 'lng', 'category', 'description', 'rating', 'photo', 'moderated']


class CityObjectModerationForm(forms.ModelForm):
    class Meta:
        model = cityObject
        fields = ['status', 'moderation_comment']
        widgets = {
            'status': forms.RadioSelect(choices=cityObject.MODERATION_STATUS),
            'moderation_comment': forms.Textarea(attrs={'rows': 3}),
        }

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