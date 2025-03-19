from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_type', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('appointment_type', 'status', 'appointment_date')
    search_fields = ('patient__username', 'doctor__last_name')