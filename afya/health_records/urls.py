from django.urls import path
from . import views

urlpatterns = [
    path('health_records/', views.enter_afya_id, name='enter_afya_id'),
    # path('health_record/<int:record_id>/', views.view_health_record, name='view_health_record'),
    # path('create_consultation/', views.create_consultation, name='create_consultation'),
    path('create_health_record/', views.create_health_record, name='create_health_record'),
    path('create_consultation/<int:appointment_id>/', views.create_consultation, name='create_consultation_with_appointment'),
    path('enter_afya_id/', views.enter_afya_id, name='enter_afya_id'),
    path('health_record_details/<str:afya_id>/', views.health_record_details, name='health_record_details'),
    path('success_url/',views.successfull_consultation,name="success_url")
    # path('view_consultation/<int:consultation_id>/', views.view_consultation, name='view_consultation'),
    
]
