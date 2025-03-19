from django.contrib import admin
from .models import Patient, HealthRecord, Consultation

admin.site.register(Patient)
admin.site.register(HealthRecord)
admin.site.register(Consultation)