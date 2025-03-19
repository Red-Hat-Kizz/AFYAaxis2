from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registration, name='register'),
    path('success/', views.successful_registration, name='success'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login_page, name='login'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]