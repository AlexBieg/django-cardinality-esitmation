from django.apps import AppConfig
from django.db import connections
from django.db.backends.signals import connection_created
from estimation.query_wrapper_utils import install_cardinality_estimation_wrapper


class EstimationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estimation'

    def ready(self):
        connection_created.connect(install_cardinality_estimation_wrapper)
        for conn in connections.all():
            install_cardinality_estimation_wrapper(conn=conn)