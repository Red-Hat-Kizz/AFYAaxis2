from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Patient, HealthRecord, Consultation
from .forms import ConsultationForm, HealthRecordForm
from django.contrib import messages
from appointments.models import Appointment
from doctors.models import Doctor
from django.contrib.auth.models import User
from notifications.models import Notification
from datetime import datetime

# View for entering Afya ID to access health records (for both patients and admins)
@login_required
def enter_afya_id(request):
    if request.method == "POST":
        entered_afya_id = request.POST.get('afya_id')
        try:
            patient = Patient.objects.get(afya_id=entered_afya_id)
            if request.user.is_staff or request.user.is_superuser:
                # Admin can access any patient's health records
                return redirect('health_record_details', afya_id=entered_afya_id)
            elif patient.user == request.user:
                # Patient can access their own health records
                return redirect('health_record_details', afya_id=entered_afya_id)
            else:
                # Patient entered an Afya ID that is not theirs
                messages.error(request, 'Incorrect Afya ID. Please enter your own Afya ID.')
                return redirect('enter_afya_id')
        except Patient.DoesNotExist:
            messages.error(request, 'Patient with that Afya ID does not exist')
            return redirect('enter_afya_id')
    return render(request, 'health_records/enter_afya_id.html')

# View for displaying health records based on Afya ID
@login_required
def health_record_details(request, afya_id):
    patient = get_object_or_404(Patient, afya_id=afya_id)
    health_records = patient.health_records.all()
    consultations = patient.consultations.all()
    
    context = {
        'patient': patient, 
        'health_records': health_records,
        'consultations': consultations
    }
    return render(request, 'health_records/patient_health_records.html', context)

# View for displaying consultation details
# health_records/views.py

@login_required
def create_consultation(request, appointment_id):
    # Get the appointment and related objects
    appointment = get_object_or_404(Appointment, id=appointment_id)
    patient = appointment.patient  # This is a User object
    doctor = appointment.doctor    # This is a Doctor object <-- FIX HERE

    print(f"Patient ID: {patient.id}, Exists: {User.objects.filter(id=patient.id).exists()}")
    print(f"Doctor ID: {doctor.id}, Exists: {Doctor.objects.filter(id=doctor.id).exists()}")
    
    consultations = Consultation.objects.filter(doctor=doctor)
    approved_appointments = Appointment.objects.filter(doctor=doctor, status='Approved')
    completed_appointments = Appointment.objects.filter(doctor=doctor, status='Completed')
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    # Get the current date and day
    current_date = datetime.now().strftime("%B %d, %Y")
    current_day = datetime.now().strftime("%A")
    
    physical_appointments_count = Appointment.objects.filter(doctor=doctor, appointment_type='Physical').count()
    virtual_appointments_count = Appointment.objects.filter(doctor=doctor, appointment_type='Virtual').count()
    
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    
    if request.method == 'POST':
        form = ConsultationForm(request.POST, request.FILES)
        if form.is_valid():
            consultation = form.save(commit=False)
            # Assign from appointment (not request.user)
            consultation.patient = patient  # User instance
            consultation.doctor = doctor    # Doctor instance <-- KEY FIX
            consultation.save()
            
            print(f"Saving Consultation: Patient={consultation.patient.id}, Doctor={consultation.doctor.id}")
            return redirect('success_url')
    else:
        # Pre-fill appointment_type from the appointment
        form = ConsultationForm(initial={'appointment_type': appointment.appointment_type})
    
    # Pass context for display
    return render(request, 'health_records/create_consultation.html', {
        'form': form,
        'patient': patient,
        'doctor': doctor,
        'consultations': consultations,
        'approved_appointments': approved_appointments,
        'unread_notifications_count': unread_notifications_count,
        'completed_appointments': completed_appointments,
        'current_date': current_date,
        'current_day': current_day,
        'physical_appointments_count': physical_appointments_count,
        'virtual_appointments_count': virtual_appointments_count,
        'notifications': notifications
    })
# View for creating a new health record
@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def create_health_record(request):
    
    if request.method == "POST":
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Health record created successfully.')
            return redirect('dashboard_home')
    else:
        form = HealthRecordForm()
    
    return render(request, 'health_records/create_health_record.html', {'form': form})

def successfull_consultation(request):
    return render(request,'health_records/success.html')