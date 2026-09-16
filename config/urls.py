from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

admin.site.site_header = 'MockLeap Admin'
admin.site.site_title = 'MockLeap'
admin.site.index_title = 'Platform management'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.core.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('reading/', include('apps.reading.urls')),
    path('listening/', include('apps.listening.urls')),
    path('writing/', include('apps.writing.urls')),
    path('speaking/', include('apps.speaking.urls')),
    path('profile/', include('apps.accounts.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
