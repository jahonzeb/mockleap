from django.contrib import admin
from .models import WritingTest, WritingTask, WritingSubmission


class WritingTaskInline(admin.StackedInline):
    model = WritingTask
    extra = 2
    fields = ('task_type', 'order', 'prompt', 'min_words', 'time_minutes', 'image')


@admin.register(WritingTest)
class WritingTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('title',)
    inlines = [WritingTaskInline]


@admin.register(WritingTask)
class WritingTaskAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'task_type', 'min_words', 'time_minutes', 'test')
    list_filter = ('task_type', 'test')


@admin.register(WritingSubmission)
class WritingSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'status', 'word_count', 'overall_band', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('created_at', 'updated_at', 'submitted_at')
    search_fields = ('user__email',)
