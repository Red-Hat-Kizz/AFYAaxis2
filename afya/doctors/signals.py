from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Doctor

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