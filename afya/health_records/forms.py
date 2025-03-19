from django import forms
from doctors.models import Doctor
from django.contrib.auth.models import User
from .models import Consultation, HealthRecord, Patient

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['notes', 'appointment_type', 'symptoms', 'diagnosis', 'treatment', 'follow_up_instructions', 'attachments']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-controltext'}),
            'appointment_type': forms.Select(attrs={'class': 'form-control'}),
            'symptoms': forms.Textarea(attrs={'class': 'form-controltext'}),
            'diagnosis': forms.Textarea(attrs={'class': 'form-controltext'}),
            'treatment': forms.Textarea(attrs={'class': 'form-controltext'}),
            'follow_up_instructions': forms.Textarea(attrs={'class': 'form-controltext'}),
            'attachments': forms.FileInput(attrs={'class': 'form-control'}),
        }

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = ['patient', 'description']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }