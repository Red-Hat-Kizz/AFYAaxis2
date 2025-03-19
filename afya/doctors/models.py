from django.db import models
from django.contrib.auth.models import User     
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone

class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    clinic = models.ForeignKey('clinics.Clinic', on_delete=models.CASCADE, related_name="doctors")
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name="doctors")
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100,default='Kenya')
    postal_code = models.CharField(max_length=10,default='0000')   
    state= models.CharField(max_length=100,default='Kisii')
    hire_date = models.DateField(null=True, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    years_worked_at_afyaaxis = models.IntegerField(null=True, blank=True)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def check_availability(self, appointment_date, appointment_time):
        # Check if the doctor has less than 3 appointments on the given date
        appointments_on_date = self.appointments.filter(appointment_date=appointment_date)
        if appointments_on_date.count() >= 3:
            return False

        # Check if the doctor has an appointment at the given time
        if appointments_on_date.filter(appointment_time=appointment_time).exists():
            return False

        return True


@receiver(post_save, sender=User)
def create_or_update_doctor_profile(sender, instance, created, **kwargs):
    if created:
        if instance.groups.filter(name='Doctors').exists():
            instance.is_staff = True
            instance.save()
            Doctor.objects.create(user=instance)
    else:
        if hasattr(instance, 'doctor_profile'):
            instance.doctor_profile.save()