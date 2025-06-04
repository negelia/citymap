from django.apps import AppConfig


class MapConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'map'

    def ready(self):
        from .models import create_permissions
        from django.db.models.signals import post_migrate
        post_migrate.connect(create_permissions, sender=self)
