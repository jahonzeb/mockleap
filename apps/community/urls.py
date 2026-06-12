from django.urls import path
from . import views

app_name = 'community'
urlpatterns = [
    path('', views.room_list, name='rooms'),
    path('<slug:slug>/', views.post_list, name='posts'),
    path('<slug:slug>/new/', views.create_post, name='create_post'),
    path('<slug:slug>/<int:pk>/', views.post_detail, name='thread'),
    path('<slug:slug>/<int:pk>/reply/', views.create_reply, name='reply'),
]
