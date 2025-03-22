from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from clinics.models import Clinic
from .models import Doctor
from appointments.models import Appointment
from django.contrib import messages
from django.core.exceptions import ValidationError
from health_records.models import HealthRecord, Consultation
from .forms import DoctorForm
import secrets
import string
from django.core.mail import send_mail
from django.conf import settings
from notifications.models import Notification   
from datetime import datetime
from django.utils import timezone

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctors/doctor_details.html', {'doctor': doctor})

# doctors dashboard====================================================================================================
@login_required
@user_passes_test(lambda u: u.is_staff and not u.is_superuser)
def doctor_dashboard(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    current_date = datetime.now().date()  # Use date() to get the date in YYYY-MM-DD format
    current_date_str = current_date.strftime("%B %d, %Y")
    current_day = datetime.now().strftime("%A")
    today = datetime.now().date()
    current_month_name = current_date.strftime("%B")
    
    approved_appointments_by_date = Appointment.objects.filter(doctor=doctor, appointment_date=current_date).order_by('-created_at')
    completed_appointments = Appointment.objects.filter(doctor=doctor, status='Completed')
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    physical_appointments_count = Appointment.objects.filter(doctor=doctor, appointment_type='Physical',status="Completed").count()
    virtual_appointments_count = Appointment.objects.filter(doctor=doctor, appointment_type='Virtual',status="Completed").count()
    
    context = {
        'doctor': doctor,
        'current_month_name':current_month_name,
        'approved_appointments_by_date': approved_appointments_by_date,
        'completed_appointments': completed_appointments,
        'unread_notifications_count': unread_notifications_count,
        'current_date': current_date_str,
        'current_day': current_day,
        'physical_appointments_count': physical_appointments_count,
        'virtual_appointments_count': virtual_appointments_count,
    }
    return render(request, 'doctors/doctor_dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_doctor(request):
    if request.method == "POST":
        doctor_form = DoctorForm(request.POST, request.FILES)
        if doctor_form.is_valid():
            # Generate a secure password
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(10))
            
            # Set the username to be the first name
            first_name = doctor_form.cleaned_data['first_name']
            username = first_name.lower()
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{first_name.lower()}{counter}"
                counter += 1
            
            # Create the user
            user = User.objects.create_user(
                username=username,
                email=doctor_form.cleaned_data['email'],
                password=password,
                is_staff=True
            )
            
            # Create the doctor
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            
            # Get admin details
            admin_full_name = f"{request.user.first_name} {request.user.last_name}"
            admin_phone_number = request.user.profile.phone_number  # Assuming the admin's phone number is stored in the profile
            
            # Send an email to the doctor with the password
            subject = 'Welcome to Afya Axis – Registration Successful'
            message = f"""
Dear Dr. {doctor.last_name},

Welcome to Afya Axis! We are thrilled to have you join our platform and look forward to working together to provide exceptional care to our patients.

Your registration has been successfully completed. Below are your login credentials:

Username: {user.username}

Password: {password}

For security reasons, we recommend that you change your password after your first login. To do so, simply:

Log in to your account using the credentials provided above.

Navigate to the "Profile" or "Account Settings" section.

Select "Change Password" and follow the prompts to set a new password.

If you have any questions or need assistance, please don’t hesitate to contact our support team at support@afyaaxis.com or {admin_phone_number}.

Once again, welcome to Afya Axis! We are excited to have you on board and look forward to collaborating with you.

Best regards,
{admin_full_name}
Afya Axis Administrator
Afya Axis
{admin_phone_number}
"""
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            messages.success(request, f'Doctor created successfully. The password has been sent to the provided email.')
            return redirect('dashboard_home')
    else:
        doctor_form = DoctorForm()
    return render(request, 'doctors/create_doctor.html', {'doctor_form': doctor_form})


@login_required
def doctor_notifications(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    doctor = request.user.doctor_profile
    doctor = get_object_or_404(Doctor, user=request.user)
    consultations = Consultation.objects.filter(doctor=doctor)
    approved_appointments = Appointment.objects.filter(doctor=doctor, status='Approved')
    completed_appointments = Appointment.objects.filter(doctor=doctor, status='Completed')
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    # Get the current date and day
    current_date = datetime.now().date()
    current_date_str = current_date.strftime("%B %d, %Y")
    current_day = datetime.now().strftime("%A")
    
    approved_appointments_by_date = Appointment.objects.filter(doctor=doctor, status='Approved', appointment_date=current_date)
    physical_appointments_count = Appointment.objects.filter(doctor=doctor, appointment_type='Physical').count()
    virtual_appointments_count = Appointment.objects.filter(doctor=doctor, appointment_type='Virtual').count()
    
    
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'doctor': doctor,
        'consultations': consultations,
        'approved_appointments': approved_appointments,
        'unread_notifications_count': unread_notifications_count,
        'completed_appointments':completed_appointments,
        'current_date': current_date_str,
        'current_day': current_day,
        'physical_appointments_count':physical_appointments_count,
        'virtual_appointments_count':virtual_appointments_count,
        'notifications':notifications,
        'approved_appointments_by_date':approved_appointments_by_date,
    }
    return render(request, 'notifications/doctor_notifications.html', context)

@login_required
def unread_notification_count(request):
    doctor = request.user.doctor_profile
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': unread_count})

@login_required
def mark_as_read_doctor(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('doctor_notifications')


@login_required
@user_passes_test(lambda u: u.is_staff and not u.is_superuser)
def mark_appointment_as_completed(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor__user=request.user)
    appointment.status = 'Completed'
    appointment.save()
    return redirect('doctor_dashboard')

@login_required
def doctor_appointments(request):
    current_date = timezone.now().date()
    current_month_name = current_date.strftime("%B")
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')
    approved_appointments = Appointment.objects.filter(doctor=doctor, status='Approved')
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
    completed_appointments = Appointment.objects.filter(doctor=doctor, status='Completed')
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'completed_appointments':completed_appointments,
        'approved_appointments':approved_appointments,
        'unread_notifications_count':unread_notifications_count,
        'current_month_name':current_month_name
    }
    return render(request, 'appointments/doctors_appointments.html', context)