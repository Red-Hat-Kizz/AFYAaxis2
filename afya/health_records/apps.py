# apps.py
from django.apps import AppConfig

class HealthRecordsConfig(AppConfig):
    name = 'health_records'

    def ready(self):
        import health_records.signals