from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.landing, name='landing'),
    path('pricing/', views.pricing, name='pricing'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('features/', views.features, name='features'),
]
