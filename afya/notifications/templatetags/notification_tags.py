from django import template
from notifications.models import Notification

register = template.Library()

@register.simple_tag(takes_context=True)
def user_unread_notifications_count(context):
    user = context['user']
    if user.is_authenticated:
        return Notification.objects.filter(user=user, is_read=False).count()
    return 0

@register.simple_tag
def all_unread_notifications_count():
    return Notification.objects.filter(is_read=False).count()