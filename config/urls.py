from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
