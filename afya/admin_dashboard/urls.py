from django.urls import path
from . import views
from health_records.views import enter_afya_id

urlpatterns = [
    path('dashboard_home/', views.dashboard_home, name='dashboard_home'),
    path('afya_doctors/', views.afya_doctors,name="afya_doctors"),
    path('afya_clinics/', views.afya_clinics,name="afya_clinics"),
    path('afya_clinics/', views.afya_clinics,name="afya_clinics"),
    path('afya_users/', views.afya_users,name="afya_users"),
    path('afya_appointments/', views.afya_appointments,name="afya_appointments"),
    path('approve_appintments/<appointment_id>/approve/', views.approve_appointment, name='approve_appointment'),
    path('reject-appointment/<int:appointment_id>/', views.reject_appointment, name='reject_appointment'),
    path('delete_notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('delete_all_notifications/', views.delete_all_notifications, name='delete_all_notifications'),
    path('mark_as_read_admin/<int:notification_id>/', views.mark_as_read_admin, name='mark_as_read_admin'),
    path('health_records/',enter_afya_id, name='enter_afya_id'),
    # Add more dashboard-specific URLs here
]