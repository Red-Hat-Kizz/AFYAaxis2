from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor
import uuid

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    afya_id = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField(auto_now_add=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    emergency_contact = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class HealthRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='health_records')
    date = models.DateField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f"Health Record for {self.patient.user.first_name} {self.patient.user.last_name} on {self.date}"

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_consultations')
    date = models.DateField(auto_now_add=True)
    notes = models.TextField()
    appointment_type = models.CharField(max_length=50, choices=[('Virtual', 'Virtual'), ('Physical', 'Physical')])
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    follow_up_instructions = models.TextField()
    attachments = models.FileField(upload_to='consultation_attachments/', blank=True, null=True)

    def __str__(self):
        return f"Consultation for {self.patient.user.first_name} {self.patient.user.last_name} with Dr. {self.doctor.user.first_name} {self.doctor.user.last_name} on {self.date}"
    
    
    
