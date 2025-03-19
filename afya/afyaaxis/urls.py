from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from afyaaxis.views import welcome_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome_page, name='welcome_page'),
    path('accounts/', include('accounts.urls')), 
    path('clinics/', include('clinics.urls')),
    path('base/', include('base.urls')),
    path('doctors/', include('doctors.urls')),  
    path('appointments/', include('appointments.urls')),
    path('admin_dashboard/', include('admin_dashboard.urls')),
    path('notifications/', include('notifications.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('health_records/', include('health_records.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)