from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.user_notifications, name='user_notifications'),
    path('admin/', views.admin_notifications, name='admin_notifications'),
    path('delete_notification/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('delete_all_notifications/', views.delete_all_notifications, name='delete_all_notifications'),
    path('mark_as_read_user/<int:notification_id>/', views.mark_as_read_user, name='mark_as_read_user'),
]