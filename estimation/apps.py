from django.apps import AppConfig
from django.db import connections
from django.db.backends.signals import connection_created


class EstimationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estimation'

    def ready(self):
        pass
