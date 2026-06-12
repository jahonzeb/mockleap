from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.profile, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('dark-mode/', views.toggle_dark_mode, name='dark_mode'),
]
