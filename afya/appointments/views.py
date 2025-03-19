from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from doctors.models import Doctor
from .forms import AppointmentForm

@login_required
def create_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.doctor = doctor
            if doctor.check_availability(appointment.appointment_date, appointment.appointment_time):
                appointment.save()
                messages.success(request, 'Appointment created successfully.')
                return redirect('user_appointment_list')
            else:
                messages.error(request, 'The doctor is not available at the selected time.')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/create_appointment.html', {'form': form, 'doctor': doctor})

@login_required
def user_appointment_list(request):
    appointments = request.user.appointments.all()
    return render(request, 'appointments/user_appointment_list.html', {'appointments': appointments})

@login_required
def admin_appointment_list(request):
    if request.user.is_staff:
        appointments = Appointment.objects.all()
        return render(request, 'appointments/admin_appointment_list.html', {'appointments': appointments})
    else:
        return redirect('user_appointment_list')

@login_required
def appointment_details(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'appointments/appointment_details.html', {'appointment': appointment})

@login_required
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.user.is_staff:
        appointment.status = 'approved'
        appointment.save()
        messages.success(request, 'Appointment approved successfully.')
    return redirect('admin_appointment_list')

@login_required
def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.user.is_staff:
        appointment.status = 'rejected'
        appointment.reject_reason = request.POST.get('reject_reason', '')
        appointment.save()
        messages.success(request, 'Appointment rejected successfully.')
    return redirect('admin_appointment_list')