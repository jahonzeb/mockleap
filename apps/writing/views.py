from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
import json
from .models import WritingTest, WritingTask, WritingSubmission


@login_required
def test_list(request):
    tests = WritingTest.objects.filter(is_published=True).prefetch_related('tasks')
    submissions = WritingSubmission.objects.filter(user=request.user).select_related('task__test')
    return render(request, 'writing/list.html', {'tests': tests, 'submissions': submissions})


@login_required
def take_test(request, task_pk):
    task = get_object_or_404(WritingTask, pk=task_pk, test__is_published=True)
    submission, _ = WritingSubmission.objects.get_or_create(
        user=request.user, task=task,
        status=WritingSubmission.STATUS_DRAFT,
        defaults={'content': ''}
    )
    return render(request, 'writing/exam.html', {'task': task, 'submission': submission})


@login_required
def autosave(request, submission_pk):
    if request.method == 'POST':
        submission = get_object_or_404(WritingSubmission, pk=submission_pk, user=request.user)
        try:
            data = json.loads(request.body)
            content = data.get('content', '')
        except Exception:
            content = request.POST.get('content', '')
        submission.content = content
        submission.word_count = len(content.split()) if content.strip() else 0
        submission.save(update_fields=['content', 'word_count', 'updated_at'])
        return HttpResponse('')
    return HttpResponse('Error', status=400)


@login_required
def submit_writing(request, submission_pk):
    if request.method == 'POST':
        submission = get_object_or_404(WritingSubmission, pk=submission_pk, user=request.user)
        content = request.POST.get('content', submission.content)
        submission.content = content
        submission.word_count = len(content.split()) if content.strip() else 0
        submission.status = WritingSubmission.STATUS_SUBMITTED
        submission.submitted_at = timezone.now()
        submission.save()
        request.user.add_xp(30)
        return redirect('writing:list')
    return redirect('writing:list')


@login_required
def submission_detail(request, submission_pk):
    submission = get_object_or_404(WritingSubmission, pk=submission_pk, user=request.user)
    return render(request, 'writing/submission_detail.html', {'submission': submission})
