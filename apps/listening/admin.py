from django.contrib import admin
from .models import ListeningTest, ListeningSection, ListeningAttempt



class ListeningSectionInline(admin.StackedInline):
    model = ListeningSection
    extra = 1
    fields = ('order', 'title', 'description', 'questions_html', 'answer_key')


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
            'duration_minutes': test.duration_minutes,
            'is_published': test.is_published,
            'audio_url': test.audio_url,
            'sections': []
        }
        for s in test.sections.all():
            test_data['sections'].append({
                'order': s.order,
                'title': s.title,
                'transcript': s.transcript,
                'description': s.description,
                'questions_html': s.questions_html,
                'answer_key': s.answer_key,
            })
        data.append(test_data)
    
    response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="listening_tests_export.json"'
    return response


@admin.register(ListeningTest)
class ListeningTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration_minutes', 'is_published', 'created_at')
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    search_fields = ('title',)
    fields = ('title', 'duration_minutes', 'audio_file', 'audio_url', 'is_published')
    inlines = [ListeningSectionInline]
    actions = [export_as_json]
    change_list_template = "admin/listening/listeningtest/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-json/', self.admin_site.admin_view(self.import_json), name='listening_test_import_json'),
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
                    test = ListeningTest.objects.create(
                        title=test_data['title'],
                        duration_minutes=test_data.get('duration_minutes', 40),
                        audio_url=test_data.get('audio_url', ''),
                        is_published=test_data.get('is_published', False)
                    )
                    for s_data in test_data.get('sections', []):
                        ListeningSection.objects.create(
                            test=test,
                            order=s_data.get('order', 1),
                            title=s_data.get('title', ''),
                            transcript=s_data.get('transcript', ''),
                            description=s_data.get('description', ''),
                            questions_html=s_data.get('questions_html', ''),
                            answer_key=s_data.get('answer_key', {})
                        )
                messages.success(request, f"Successfully imported {len(data)} tests.")
                return redirect("..")
            except Exception as e:
                messages.error(request, f"Import error: {str(e)}")
                return redirect("..")
        
        return render(request, "admin/import_json.html", {"title": "Import Listening Tests", "app_label": "listening", "model_name": "listeningtest"})


@admin.register(ListeningSection)
class ListeningSectionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order', 'title', 'test')
    list_filter = ('test',)
    fields = ('test', 'order', 'title', 'description', 'questions_html', 'answer_key')


@admin.register(ListeningAttempt)
class ListeningAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'status', 'score_raw', 'band_score', 'submitted_at')
    list_filter = ('status',)
    readonly_fields = ('answers', 'started_at', 'submitted_at')

