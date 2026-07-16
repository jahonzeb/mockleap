from django.urls import path
from . import views

app_name = 'reading'
urlpatterns = [
    path('', views.test_list, name='list'),
    path('<int:pk>/exam/', views.take_test, name='exam'),
    path('attempt/<int:attempt_pk>/autosave/', views.autosave, name='autosave'),
    path('attempt/<int:attempt_pk>/submit/', views.submit_test, name='submit'),
    path('results/<int:attempt_pk>/', views.results, name='results'),
    path('<int:pk>/quick-edit/', views.quick_edit, name='quick_edit'),
    path('<int:pk>/delete/', views.delete_test, name='delete'),
    path('<int:pk>/export/', views.export_test_json, name='export'),
]
