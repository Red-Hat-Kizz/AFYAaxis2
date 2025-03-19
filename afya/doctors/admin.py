from django.contrib import admin
from .models import Specialization, Doctor

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'clinic', 'specialization')
    list_filter = ('clinic', 'specialization')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'clinic__name', 'specialization__name')

# Alternatively, you can use admin.site.register without the decorator
# admin.site.register(Specialization, SpecializationAdmin)
# admin.site.register(Doctor, DoctorAdmin)s