from django.shortcuts import render
from doctors.models import Doctor, Specialization  # Import the Specialization model
from accounts.models import Profile
from clinics.models import Clinic, Service  # Import the Service model
from django.db.models import Q

def home(request):
    profile = Profile.objects.get(user=request.user)
    doctors = Doctor.objects.all()
    context = {
        'doctors': doctors,
        'profile': profile
    }
    return render(request, 'base/home.html', context)

def search(request):
    query = request.GET.get('q')
    if query:
        doctors = Doctor.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(specialization__name__icontains=query)
        )
        clinics = Clinic.objects.filter(
            Q(name__icontains=query) | Q(address__icontains=query) | Q(services__name__icontains=query)
        ).distinct()
        services = Service.objects.filter(
            Q(name__icontains=query)
        )
        specializations = Specialization.objects.filter(
            Q(name__icontains=query)
        )
    else:
        doctors = Doctor.objects.all()
        clinics = Clinic.objects.all()
        services = Service.objects.all()
        specializations = Specialization.objects.all()
    
    
    services_with_clinics = []
    for service in services:
        service_clinics = service.clinics.all()[:3]
        services_with_clinics.append((service,service_clinics))
    
    
    context = {
        'doctors': doctors,
        'clinics': clinics,
        'services': services,
        'services_with_clinics': services_with_clinics,
        'specializations': specializations,
        'query': query,
    }
    return render(request, 'base/search_results.html', context)