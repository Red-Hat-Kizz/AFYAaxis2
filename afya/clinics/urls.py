from django.urls import path
from . import views

urlpatterns = [
    path('', views.clinic_list, name='clinic_list'),
    path('<int:clinic_id>/', views.clinic_detail, name='clinic_detail'),
    path('services/', views.service_list, name='service_list'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('create_clinic/', views.create_clinic, name='create_clinic'),
]