from django.apps import AppConfig


class NewsportalappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Newsportalapp'

    def ready(self):
        from . import signals
