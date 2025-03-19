from django.urls import path
from . import views
from notifications.views import delete_notification, delete_all_notifications

urlpatterns = [
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('create_doctor/', views.create_doctor, name='create_doctor'),
    path('doctor_notifications/', views.doctor_notifications, name='doctor_notifications'),
    path('unread_notification_count/', views.unread_notification_count, name='unread_notification_count'),
    path('mark_notification_as_read_doctor/<int:notification_id>/', views.mark_as_read_doctor, name='mark_notification_as_read_doctor'),
    path('delete_notification/<int:notification_id>/', delete_notification, name='delete_notification'),
    path('delete_all_notifications/', delete_all_notifications, name='delete_all_notifications'),
    path('mark_appointment_as_completed/<int:appointment_id>/', views.mark_appointment_as_completed, name='mark_appointment_as_completed'),
     path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    # path('specialties/', views.specialty_list, name='specialty_list'),
    # path('specialties/<int:specialty_id>/', views.specialty_detail, name='specialty_detail'),
]