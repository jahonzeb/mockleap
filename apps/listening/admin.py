from django.contrib import admin
from .models import ListeningTest, ListeningSection, ListeningQuestion, ListeningAttempt


class ListeningQuestionInline(admin.TabularInline):
    model = ListeningQuestion
    extra = 4
    fields = ('number', 'text', 'question_type', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')


class ListeningSectionInline(admin.StackedInline):
    model = ListeningSection
    extra = 1
    fields = ('order', 'title', 'description')
    show_change_link = True


@admin.register(ListeningTest)
class ListeningTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration_minutes', 'is_published', 'created_at')
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    search_fields = ('title',)
    fields = ('title', 'duration_minutes', 'audio_file', 'is_published')
    inlines = [ListeningSectionInline]


@admin.register(ListeningSection)
class ListeningSectionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order', 'title', 'test')
    list_filter = ('test',)
    inlines = [ListeningQuestionInline]


@admin.register(ListeningQuestion)
class ListeningQuestionAdmin(admin.ModelAdmin):
    list_display = ('number', 'text', 'question_type', 'correct_answer')
    list_filter = ('question_type', 'section__test')
    search_fields = ('text',)


@admin.register(ListeningAttempt)
class ListeningAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'status', 'score_raw', 'band_score', 'submitted_at')
    list_filter = ('status',)
    readonly_fields = ('answers', 'started_at', 'submitted_at')
