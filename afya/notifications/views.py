from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Notification

@login_required
def user_notifications(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    context = {
        'notifications': notifications
    }
    return render(request, 'notifications/user_notifications.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'notifications': notifications
    }
    return render(request, 'notifications/admin_notifications.html', context)

@login_required
def mark_as_read_user(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('user_notifications')

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def mark_as_read_admin(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('admin_notifications')

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    if request.user == notification.user or request.user.is_staff:
        notification.delete()
        if request.user.is_superuser:
            return redirect('admin_notifications')
        elif hasattr(request.user, 'doctor_profile'):
            return redirect('doctor_notifications')
        else:
            return redirect('user_notifications')
    else:
        return redirect('user_notifications')

@login_required
def delete_all_notifications(request):
    if request.user.is_superuser:
        Notification.objects.filter(user=request.user).delete()
        return redirect('admin_notifications')
    elif hasattr(request.user, 'doctor_profile'):
        Notification.objects.filter(user=request.user).delete()
        return redirect('doctor_notifications')
    else:
        request.user.notifications.all().delete()
        return redirect('user_notifications')