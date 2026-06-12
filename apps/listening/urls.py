from django.urls import path
from . import views

app_name = 'listening'
urlpatterns = [
    path('', views.test_list, name='list'),
    path('<int:pk>/exam/', views.take_test, name='exam'),
    path('attempt/<int:attempt_pk>/submit/', views.submit_test, name='submit'),
    path('results/<int:attempt_pk>/', views.results, name='results'),
]
