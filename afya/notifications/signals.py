import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from appointments.models import Appointment
from .models import Notification
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Appointment)
def send_notification(sender, instance, created, **kwargs):
    if created:
        # Notify admin when a new appointment is created
        admin_users = User.objects.filter(is_staff=True)
        profile_picture_url = instance.patient.profile.profile_picture.url if instance.patient.profile.profile_picture else ''
        for admin in admin_users:
            Notification.objects.create(
                user=admin,
                message=f"New appointment request from {instance.patient.username} ({instance.patient.first_name} {instance.patient.last_name})",
                profile_picture_url=profile_picture_url,
                doctor_name=f"Dr. {instance.doctor.first_name} {instance.doctor.last_name}",
                clinic_name=instance.doctor.clinic.name,
                appointment_date=instance.appointment_date,
                appointment_time=instance.appointment_time,
                appointment_type=instance.get_appointment_type_display(),
                applicant_username=instance.patient.username,
                applicant_first_name=instance.patient.first_name,
                applicant_last_name=instance.patient.last_name
            )
            logger.info(f"Notification created for admin: {admin.username}")
    else:
        # Notify user when their appointment is approved or rejected
        admin_user = kwargs.get('admin_user')
        admin_profile_picture_url = ''
        if admin_user and hasattr(admin_user, 'profile') and admin_user.profile.profile_picture:
            admin_profile_picture_url = admin_user.profile.profile_picture.url
        if instance.status == 'Approved':
            # Notify the patient
            Notification.objects.create(
                user=instance.patient,
                message="Your appointment has been approved.",
                profile_picture_url=admin_profile_picture_url,
                doctor_name=f"Dr. {instance.doctor.first_name} {instance.doctor.last_name}",
                clinic_name=instance.doctor.clinic.name,
                appointment_date=instance.appointment_date,
                appointment_time=instance.appointment_time,
                appointment_type=instance.get_appointment_type_display()
            )
            logger.info(f"Notification created for user: {instance.patient.username} (Approved)")

            # Notify the doctor
            Notification.objects.create(
                user=instance.doctor.user,
                message=f"Appointment with {instance.patient.first_name} {instance.patient.last_name} on {instance.appointment_date} at {instance.appointment_time} has been approved.",
                profile_picture_url=instance.patient.profile.profile_picture.url if instance.patient.profile.profile_picture else '',
                doctor_name=f"Dr. {instance.doctor.first_name} {instance.doctor.last_name}",
                clinic_name=instance.doctor.clinic.name,
                appointment_date=instance.appointment_date,
                appointment_time=instance.appointment_time,
                appointment_type=instance.get_appointment_type_display()
            )
            logger.info(f"Notification created for doctor: {instance.doctor.user.username} (Approved)")
        elif instance.status == 'Rejected':
            Notification.objects.create(
                user=instance.patient,
                message="Your appointment has been rejected.",
                rejection_reason=instance.rejection_reason,
                profile_picture_url=admin_profile_picture_url
            )
            logger.info(f"Notification created for user: {instance.patient.username} (Rejected)")