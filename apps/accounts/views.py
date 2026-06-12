from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.bio = request.POST.get('bio', user.bio)
        user.country = request.POST.get('country', user.country)
        target = request.POST.get('target_band')
        if target:
            user.target_band = float(target)
        test_date = request.POST.get('test_date')
        if test_date:
            user.test_date = test_date
        user.dark_mode = request.POST.get('dark_mode') == 'on'
        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']
        user.save()
        messages.success(request, 'Profile updated.')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html')

@login_required
def settings_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.bio = request.POST.get('bio', user.bio)
        user.country = request.POST.get('country', user.country)
        target = request.POST.get('target_band')
        if target:
            user.target_band = float(target)
        test_date = request.POST.get('test_date')
        if test_date:
            user.test_date = test_date
        user.dark_mode = request.POST.get('dark_mode') == 'on'
        user.email_notifications = request.POST.get('email_notifications') == 'on'
        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:settings')
    return render(request, 'accounts/settings.html')


@login_required
def toggle_dark_mode(request):
    if request.method == 'POST':
        dark = request.POST.get('dark') == '1'
        request.user.dark_mode = dark
        request.user.save(update_fields=['dark_mode'])
        return HttpResponse('')
    return HttpResponse('Error', status=400)
