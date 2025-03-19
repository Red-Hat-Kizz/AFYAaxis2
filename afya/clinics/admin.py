from django.contrib import admin
from .models import Clinic, Service, OpeningHours

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)

class OpeningHoursInline(admin.TabularInline):
    model = OpeningHours
    extra = 1  # Show an extra empty form for new entries

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'website')
    list_filter = ('services',)
    search_fields = ('name', 'address', 'phone_number')
    inlines = [OpeningHoursInline]  # Add OpeningHours inline for each Clinic

admin.site.register(OpeningHours)
