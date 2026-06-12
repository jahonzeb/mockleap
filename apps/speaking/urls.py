from django.urls import path
from . import views

app_name = 'speaking'
urlpatterns = [
    path('', views.test_list, name='list'),
    path('part/<int:part_pk>/exam/', views.take_test, name='exam'),
    path('part/<int:part_pk>/submit/', views.submit_recording, name='submit'),
    path('part/<int:part_pk>/upload/', views.upload_recording, name='upload'),
    path('submission/<int:submission_pk>/', views.submission_detail, name='detail'),
]
