from django.db import models

class cityObject(models.Model):
    CATEGORY_CHOICES = [
        ('toilet', 'Санузел'),
        ('water', 'Пополнение воды'),
        ('rest', 'Зона отдыха'),
    ]
    
    lng = models.FloatField()
    lat = models.FloatField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='markers/', blank=True, null=True)
    rating = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    moderated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'map_cityobject'