from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Notification


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'notifications/list.html', {'notifications': notifications})


@login_required
def mark_read(request, pk):
    if request.method == 'POST':
        Notification.objects.filter(pk=pk, user=request.user).update(is_read=True)
        return HttpResponse('')
    return HttpResponse('Error', status=400)
