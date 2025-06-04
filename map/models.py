from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

User = get_user_model()

class cityObject(models.Model):
    CATEGORY_CHOICES = [
        ('toilet', 'Санузел'),
        ('water', 'Пополнение воды'),
        ('rest', 'Зона отдыха'),
    ]

    MODERATION_STATUS = (
        ('pending', 'На модерации'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    )
    
    lng = models.FloatField()
    lat = models.FloatField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='markers/', blank=True, null=True)
    rating = models.IntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    moderated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=10,
        choices=MODERATION_STATUS,
        default='pending',
        verbose_name='Статус модерации'
    )
    moderator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moderated_points',
        verbose_name='Модератор'
    )
    moderation_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Дата модерации'
    )
    moderation_comment = models.TextField(
        blank=True,
        verbose_name='Комментарий модератора'
    )
    
    def __str__(self):
        return self.title
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_objects'
    )
    
    class Meta:
        permissions = [
            ("can_moderate_cityobjects", "Can moderate city objects"),
        ]

@receiver(post_migrate)
def create_permissions(sender, **kwargs):
    if sender.name == 'map':
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        
        content_type = ContentType.objects.get_for_model(cityObject)
        Permission.objects.get_or_create(
            codename='can_moderate_cityobjects',
            name='Can moderate city objects',
            content_type=content_type,
        )