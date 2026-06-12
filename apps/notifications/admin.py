from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('user__email', 'title')
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'
    actions = ['mark_all_read']

    @admin.action(description='Mark selected as read')
    def mark_all_read(self, request, queryset):
        queryset.update(is_read=True)
