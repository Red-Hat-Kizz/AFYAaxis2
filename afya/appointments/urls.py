from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:doctor_id>/', views.create_appointment, name='create_appointment'),
    path('user_list/', views.user_appointment_list, name='user_appointment_list'),
    path('admin_list/', views.admin_appointment_list, name='admin_appointment_list'),
    path('details/<int:appointment_id>/', views.appointment_details, name='appointment_details'),
    path('approve/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('reject/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
]