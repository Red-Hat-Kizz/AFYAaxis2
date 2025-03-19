from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib import messages 
from . forms import SignUpForm,LoginForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm



# Create your views here.
def registration(request):
    if request.method == "POST":
        form= SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
           # Get the user's profile and afya_id
            profile = user.profile
            afya_id = profile.afya_id

            # Send email with afya_id
            send_mail(
                'Your Afya ID',
                f'Your Afya ID is: {afya_id}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return redirect("success")
        else:
            print(form.errors)  # Debugging: Print form errors
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = SignUpForm()
    context = {
        'form':form
    }
    return render(request,'accounts/register.html',context)

def successful_registration(request):
    return render(request,'email/success_registration.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('welcome_page')



def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request, user)
                if user.is_staff and not user.is_superuser and hasattr(user, 'doctor_profile'):
                    return redirect('doctor_dashboard')
                elif user.is_superuser:
                    return redirect('dashboard_home')
                else:
                    return redirect('home')
            else:
                form.add_error(None,"Invalid username or password")
    
    else:
        form = LoginForm()
    context = {
        'form':form
    }
    return render(request,'accounts/login.html',context)


@login_required
def profile_view(request):
    """View to display the user's profile."""
    profile = request.user.profile
    allergies = profile.allergies.split(',') if profile.allergies else []
    chronic_conditions = profile.chronic_conditions.split(',') if profile.chronic_conditions else []
    return render(request, 'accounts/user_profile.html', {
        'profile': profile,
        'allergies': allergies,
        'chronic_conditions': chronic_conditions,})

@login_required
def edit_profile(request):
    """View to edit the user's profile."""
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # Redirect to the profile view after saving
    else:
        form = ProfileForm(instance=profile)
        context = {
        'form': form,
        }
    return render(request, 'accounts/profile_edit.html', context)