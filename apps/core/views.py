from django.shortcuts import render, redirect


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return render(request, 'core/landing.html')


def pricing(request):
    return render(request, 'core/pricing.html')


def about(request):
    return render(request, 'core/about.html')


def faq(request):
    return render(request, 'core/faq.html')


def features(request):
    return render(request, 'core/features.html')


def not_found(request, exception=None):
    return render(request, 'core/404.html', status=404)
