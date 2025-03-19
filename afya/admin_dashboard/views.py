from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils import timezone
from doctors.models import Doctor
from appointments.models import Appointment
from clinics.models import Clinic
from accounts.models import Profile
from django.shortcuts import render, get_object_or_404, redirect
from notifications.models import Notification
from django.db.models.signals import post_save
from accounts.models import Profile


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def dashboard_home(request):
    profile = Profile.objects.all()
    users = User.objects.all().select_related('profile')
    today = timezone.now().date()
    clinics_count = Clinic.objects.all().count()
    doctors_count = Doctor.objects.all().count()
    doctors = Doctor.objects.all()
    today_appointments = Appointment.objects.filter(created_at__date=today)
    today_appointments_count = today_appointments.count()
    approved_today = Appointment.objects.filter(
        created_at__date=today,  # Filter by today's date
        status='Approved'        # Filter by approved status
    )
    approved_today_count = approved_today.count()
    user_count = User.objects.count()
    recent_users = User.objects.order_by('-date_joined')[:5]
    notifications = Notification.objects.all().order_by('-created_at')

    context = {
        'users': users,
        'profile':profile,
        'today_appointments': today_appointments,
        'today_appointments_count': today_appointments_count,
        'approved_today': approved_today,
        'approved_today_count': approved_today_count,
        'doctors': doctors,
        'clinics_count': clinics_count,
        'doctors_count': doctors_count,
        'user_count': user_count,
        'recent_users': recent_users,
        'notifications': notifications,
    }
    return render(request, 'admin/dashboard.html', context)

# d0octors===================================
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def afya_doctors(request):
    doctors = Doctor.objects.all()
    context ={
        'doctors':doctors
    }
    return render(request,'admin/doctors.html',context)

def afya_clinics(request):
    clinics = Clinic.objects.all()
    doctors =Doctor.objects.all()
    context ={
        'clinics':clinics,
        'doctor':doctors,
    }
    return render(request,'admin/clinics.html',context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def afya_users(request):
    users = User.objects.all().select_related('profile')
    doctors =Doctor.objects.all()
    context = {
        'users':users,
        'doctor':doctors,
    }
    return render(request,'admin/registered_users.html',context)

# appointments===========================
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def afya_appointments(request):
    appointments = Appointment.objects.select_related(
        'patient',
        'doctor'
    ).all().order_by('-created_at')
    
    context ={
        'appointments':appointments
    }
    return render(request,'admin/appointment_list.html',context)


@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Approved'
    appointment.save()
    return redirect('afya_appointments')

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Rejected'
    appointment.rejection_reason = request.POST.get('rejection_reason', '')
    appointment.save(update_fields=['status', 'rejection_reason'])
    # Trigger the signal with the admin user
    post_save.send(sender=Appointment, instance=appointment, created=False, admin_user=request.user)
    return redirect('afya_appointments')

# def reject_appointment(request, appointment_id):
#     if request.method == 'POST':
#         appointment = get_object_or_404(Appointment, id=appointment_id)
#         appointment.status = 'Cancelled'
#         appointment.rejection_reason = request.POST.get('rejection_reason', '')
#         appointment.save()
#     return redirect('appointments_list')

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    if request.user == notification.user or request.user.is_staff:
        notification.delete()
        if request.user.is_staff:
            return redirect('admin_notifications')
        else:
            return redirect('user_notifications')
    else:
        return redirect('user_notifications')

@login_required
def delete_all_notifications(request):
    if request.user.is_staff or request.user.is_superuser:
        Notification.objects.all().delete()
        return redirect('admin_notifications')
    else:
        request.user.notifications.all().delete()
        return redirect('user_notifications')
    
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def mark_as_read_admin(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('admin_notifications')



# health records================================
