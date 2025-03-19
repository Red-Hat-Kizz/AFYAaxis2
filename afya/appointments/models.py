from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor

class Appointment(models.Model):
    APPOINTMENT_TYPE_CHOICES = [
        ('virtual', 'Virtual'),
        ('physical', 'Physical'),
    ]

    APPOINTMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_type = models.CharField(max_length=10, choices=APPOINTMENT_TYPE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=10, choices=APPOINTMENT_STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Add this line

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.last_name} on {self.appointment_date} at {self.appointment_time}"
    
    def check_availability(self, date, time):
        # Check if the doctor is available at the given date and time
        return not Appointment.objects.filter(doctor=self.doctor, appointment_date=date, appointment_time=time).exists()
