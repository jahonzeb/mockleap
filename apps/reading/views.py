from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
import json
from .models import ReadingTest, ReadingAttempt


@login_required
def test_list(request):
    tests = ReadingTest.objects.filter(is_published=True)
    attempts = ReadingAttempt.objects.filter(user=request.user).select_related('test')
    return render(request, 'reading/list.html', {'tests': tests, 'attempts': attempts})


@login_required
def take_test(request, pk):
    test = get_object_or_404(ReadingTest, pk=pk, is_published=True)
    attempt, _ = ReadingAttempt.objects.get_or_create(
        user=request.user, test=test,
        status=ReadingAttempt.STATUS_IN_PROGRESS,
        defaults={'answers': {}}
    )
    passages = test.passages.prefetch_related('question_groups__questions').all()
    return render(request, 'reading/exam.html', {
        'test': test,
        'attempt': attempt,
        'passages': passages,
        'tfng_values': ['True', 'False', 'Not Given'],
    })


@login_required
def autosave(request, attempt_pk):
    if request.method == 'POST':
        attempt = get_object_or_404(ReadingAttempt, pk=attempt_pk, user=request.user)
        try:
            data = json.loads(request.body)
            answers = {k[1:]: v for k, v in data.items() if k.startswith('q')}
        except Exception:
            answers = {k[1:]: v for k, v in request.POST.items() if k.startswith('q')}
        attempt.answers = answers
        attempt.save(update_fields=['answers'])
        return HttpResponse('')
    return HttpResponse('Error', status=400)


@login_required
def submit_test(request, attempt_pk):
    if request.method == 'POST':
        attempt = get_object_or_404(ReadingAttempt, pk=attempt_pk, user=request.user)
        # Collect answers: form posts name="q{question.pk}"
        answers = {}
        for key, value in request.POST.items():
            if key.startswith('q') and key[1:].isdigit():
                answers[key[1:]] = value.strip()
        attempt.answers = answers
        attempt.status = ReadingAttempt.STATUS_SUBMITTED
        attempt.submitted_at = timezone.now()
        # Auto-grade by question pk
        correct = 0
        total = 0
        for passage in attempt.test.passages.all():
            for group in passage.question_groups.all():
                for q in group.questions.all():
                    total += 1
                    given = answers.get(str(q.pk), '').lower()
                    if given == q.correct_answer.strip().lower():
                        correct += 1
        attempt.score_raw = correct
        pct = correct / max(total, 1)
        attempt.band_score = round(pct * 9 * 2) / 2  # round to nearest 0.5
        attempt.save()
        request.user.add_xp(50)
        return redirect('reading:results', attempt_pk=attempt.pk)
    return redirect('reading:list')


@login_required
def results(request, attempt_pk):
    attempt = get_object_or_404(ReadingAttempt, pk=attempt_pk, user=request.user)
    return render(request, 'reading/results.html', {'attempt': attempt})
