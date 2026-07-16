from django.contrib import admin
from .models import ReadingTest, ReadingPassage, ReadingAttempt


class ReadingPassageInline(admin.StackedInline):
    model = ReadingPassage
    extra = 1
    fields = ('order', 'title', 'content', 'source')


class ReadingPassageInline(admin.StackedInline):
    model = ReadingPassage
    extra = 1
    fields = ('order', 'title', 'content', 'source', 'questions_html', 'answer_key')


import json
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

@admin.action(description='Export selected tests as JSON')
def export_as_json(modeladmin, request, queryset):
    data = []
    for test in queryset:
        test_data = {
            'title': test.title,
            'test_type': getattr(test, 'test_type', 'academic'),
            'duration_minutes': test.duration_minutes,
            'is_published': test.is_published,
            'passages': []
        }
        for p in test.passages.all():
            test_data['passages'].append({
                'order': p.order,
                'title': p.title,
                'content': p.content,
                'source': p.source,
                'questions_html': p.questions_html,
                'answer_key': p.answer_key,
            })
        data.append(test_data)
    
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="reading_tests_export.json"'
    return response


@admin.register(ReadingTest)
class ReadingTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'test_type', 'duration_minutes', 'is_published', 'created_at')
    list_filter = ('test_type', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('title',)
    inlines = [ReadingPassageInline]
    actions = [export_as_json]
    change_list_template = "admin/reading/readingtest/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-json/', self.admin_site.admin_view(self.import_json), name='reading_test_import_json'),
        ]
        return custom_urls + urls

    def import_json(self, request):
        if request.method == "POST":
            json_file = request.FILES.get("json_file")
            if not json_file:
                messages.error(request, "No file uploaded.")
                return redirect("..")
            try:
                data = json.loads(json_file.read().decode('utf-8'))
                for test_data in data:
                    test = ReadingTest.objects.create(
                        title=test_data['title'],
                        test_type=test_data.get('test_type', 'academic'),
                        duration_minutes=test_data.get('duration_minutes', 60),
                        is_published=test_data.get('is_published', False),
                        created_by=request.user
                    )
                    for p_data in test_data.get('passages', []):
                        ReadingPassage.objects.create(
                            test=test,
                            order=p_data.get('order', 1),
                            title=p_data.get('title', ''),
                            content=p_data.get('content', ''),
                            source=p_data.get('source', ''),
                            questions_html=p_data.get('questions_html', ''),
                            answer_key=p_data.get('answer_key', {})
                        )
                messages.success(request, f"Successfully imported {len(data)} tests.")
                return redirect("..")
            except Exception as e:
                messages.error(request, f"Import error: {str(e)}")
                return redirect("..")
        
        return render(request, "admin/import_json.html", {"title": "Import Reading Tests", "app_label": "reading", "model_name": "readingtest"})



@admin.register(ReadingPassage)
class ReadingPassageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order', 'title', 'test')
    list_filter = ('test',)
    fields = ('test', 'order', 'title', 'source', 'content', 'questions_html', 'answer_key')


@admin.register(ReadingAttempt)
class ReadingAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'status', 'score_raw', 'band_score', 'submitted_at')
    list_filter = ('status',)
    readonly_fields = ('answers', 'started_at', 'submitted_at')

