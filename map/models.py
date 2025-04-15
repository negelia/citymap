from django.db import models

class cityObject(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()
    approved = models.BooleanField(default=False) 
