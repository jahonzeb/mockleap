from django.urls import path
from . import views

app_name = 'teachers'
urlpatterns = [
    # Review queue
    path('', views.dashboard, name='dashboard'),
    path('writing/<int:submission_pk>/review/', views.review_writing, name='review_writing'),
    path('speaking/<int:submission_pk>/review/', views.review_speaking, name='review_speaking'),

    # Reading content management
    path('reading/', views.reading_tests, name='reading_tests'),
    path('reading/<int:pk>/', views.reading_test_edit, name='reading_test_edit'),
    path('reading/passage/<int:pk>/', views.reading_passage_edit, name='reading_passage_edit'),

    # Listening content management
    path('listening/', views.listening_tests, name='listening_tests'),
    path('listening/<int:pk>/', views.listening_test_edit, name='listening_test_edit'),
    path('listening/section/<int:pk>/', views.listening_section_edit, name='listening_section_edit'),
]
