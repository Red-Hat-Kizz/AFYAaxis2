from django.shortcuts import render, get_object_or_404,redirect
from .models import Clinic, Service
from django.contrib.auth.decorators import login_required, user_passes_test 
from django.utils.timezone import localtime
from .forms import ClinicForm

def clinic_list(request):
    clinics = Clinic.objects.all()
    return render(request, 'clinics/clinic_list.html', {'clinics': clinics})

def clinic_detail(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    doctors = clinic.doctors.all()
    current_day_hours = clinic.get_current_day_hours()
    is_open = clinic.is_open_now()
    
    return render(request, 'clinics/clinic_detail.html', {
        'clinic': clinic,
         'doctors': doctors,
        "current_day_hours": current_day_hours,
        "is_open": is_open})

def service_list(request):
    services = Service.objects.all()
    return render(request, 'clinics/service_list.html', {'services': services})

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'clinics/service_detail.html', {'service': service})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_clinic(request):
    if request.method == "POST":
        form = ClinicForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Clinic created successfully.')
            return redirect('dashboard_home')
    else:
        form = ClinicForm()
    return render(request, 'clinics/create_clinic.html', {'form': form})