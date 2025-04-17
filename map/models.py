from django.db import models

class cityObject(models.Model):
    OBJECT_TYPES = [
        ('toilet', 'Санузел'),
        ('water_refill', 'Пополнение воды'),
        ('rest_area', 'Зона отдыха'),
    ]
    
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()
    approved = models.BooleanField(default=False)
    object_type = models.CharField(
        max_length=20,
        choices=OBJECT_TYPES,
        default='toilet',
    )

    def __str__(self):
        return self.name
