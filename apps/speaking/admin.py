from django.contrib import admin
from .models import SpeakingTest, SpeakingPart, SpeakingSubmission


class SpeakingPartInline(admin.StackedInline):
    model = SpeakingPart
    extra = 3
    fields = ('part_type', 'order', 'prompt', 'cue_card_points', 'prep_time_seconds', 'speak_time_seconds')


@admin.register(SpeakingTest)
class SpeakingTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('title',)
    inlines = [SpeakingPartInline]


@admin.register(SpeakingPart)
class SpeakingPartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'part_type', 'prep_time_seconds', 'speak_time_seconds', 'test')
    list_filter = ('part_type', 'test')


@admin.register(SpeakingSubmission)
class SpeakingSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'part', 'status', 'overall_band', 'submitted_at')
    list_filter = ('status',)
    readonly_fields = ('submitted_at',)
