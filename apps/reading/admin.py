from django.contrib import admin
from .models import ReadingTest, ReadingPassage, QuestionGroup, Question, ReadingAttempt


class ReadingPassageInline(admin.StackedInline):
    model = ReadingPassage
    extra = 1
    fields = ('order', 'title', 'content', 'source')


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3
    fields = ('number', 'text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')


class QuestionGroupInline(admin.StackedInline):
    model = QuestionGroup
    extra = 1
    fields = ('order', 'question_type', 'instructions')
    show_change_link = True


@admin.register(ReadingTest)
class ReadingTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'test_type', 'duration_minutes', 'is_published', 'created_at')
    list_filter = ('test_type', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title',)
    inlines = [ReadingPassageInline]


@admin.register(ReadingPassage)
class ReadingPassageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order', 'title')
    list_filter = ('test',)
    inlines = [QuestionGroupInline]


@admin.register(QuestionGroup)
class QuestionGroupAdmin(admin.ModelAdmin):
    list_display = ('passage', 'question_type', 'order')
    list_filter = ('question_type',)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('number', 'text', 'correct_answer', 'group')
    list_filter = ('group__passage__test',)
    search_fields = ('text',)


@admin.register(ReadingAttempt)
class ReadingAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'status', 'score_raw', 'band_score', 'submitted_at')
    list_filter = ('status',)
    readonly_fields = ('answers', 'started_at', 'submitted_at')
