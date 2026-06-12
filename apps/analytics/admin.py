from django.contrib import admin
from .models import DailyActivity


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'reading_minutes', 'listening_minutes', 'writing_minutes', 'speaking_minutes', 'total_minutes')
    list_filter = ('date',)
    search_fields = ('user__email',)
    date_hierarchy = 'date'
    readonly_fields = ('date',)
