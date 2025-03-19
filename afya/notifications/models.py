from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    profile_picture_url = models.URLField(blank=True, null=True)
    doctor_name = models.CharField(max_length=255, blank=True, null=True)
    clinic_name = models.CharField(max_length=255, blank=True, null=True)
    appointment_date = models.DateField(blank=True, null=True)
    appointment_time = models.TimeField(blank=True, null=True)
    appointment_type = models.CharField(max_length=255, blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    applicant_username = models.CharField(max_length=255, blank=True, null=True)  # Add this field
    applicant_first_name = models.CharField(max_length=255, blank=True, null=True)  # Add this field
    applicant_last_name = models.CharField(max_length=255, blank=True, null=True)  # Add this field

    def __str__(self):
        return f"Notification for {self.user.username}"