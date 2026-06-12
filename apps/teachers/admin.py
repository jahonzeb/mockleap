from django.contrib import admin
from .models import TeacherProfile


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specializations', 'hourly_rate', 'avg_rating', 'total_reviews', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('user__email', 'specializations')
