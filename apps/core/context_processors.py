from django.conf import settings


def site_context(request):
    ctx = {
        'brand': getattr(settings, 'MOCKLEAP_BRAND', 'MockLeap'),
        'dark_mode': getattr(request.user, 'dark_mode', False) if request.user.is_authenticated else False,
        'unread_count': 0,
    }
    if request.user.is_authenticated:
        try:
            from apps.notifications.models import Notification
            ctx['unread_count'] = Notification.objects.filter(user=request.user, is_read=False).count()
        except Exception:
            pass
    return ctx
