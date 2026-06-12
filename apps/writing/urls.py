from django.urls import path
from . import views

app_name = 'writing'
urlpatterns = [
    path('', views.test_list, name='list'),
    path('task/<int:task_pk>/exam/', views.take_test, name='exam'),
    path('submission/<int:submission_pk>/autosave/', views.autosave, name='autosave'),
    path('submission/<int:submission_pk>/submit/', views.submit_writing, name='submit'),
    path('submission/<int:submission_pk>/', views.submission_detail, name='detail'),
]
