from django import forms
from .models import cityObject

class cityObjectForm(forms.ModelForm):
    class Meta:
        model = cityObject
        fields = ['name', 'lat', 'lon']