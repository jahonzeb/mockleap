from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import ListeningTest, ListeningAttempt


@login_required
def test_list(request):
    tests = ListeningTest.objects.filter(is_published=True)
    return render(request, 'listening/list.html', {'tests': tests})


@login_required
def take_test(request, pk):
    test = get_object_or_404(ListeningTest, pk=pk, is_published=True)
    attempt, _ = ListeningAttempt.objects.get_or_create(
        user=request.user, test=test,
        status=ListeningAttempt.STATUS_IN_PROGRESS,
        defaults={'answers': {}}
    )
    return render(request, 'listening/exam.html', {'test': test, 'attempt': attempt})


@login_required
def submit_test(request, attempt_pk):
    if request.method == 'POST':
        attempt = get_object_or_404(ListeningAttempt, pk=attempt_pk, user=request.user)
        # Collect answers from HTML form: name="q{question.pk}"
        answers = {}
        for key, value in request.POST.items():
            if key.startswith('q') and key[1:].isdigit():
                answers[key[1:]] = value.strip()
        attempt.answers = answers
        attempt.status = ListeningAttempt.STATUS_SUBMITTED
        attempt.submitted_at = timezone.now()
        # Auto-grade
        correct = 0
        total = 0
        for sec in attempt.test.sections.all():
            for q in sec.questions.all():
                total += 1
                given = answers.get(str(q.pk), '').lower()
                if given == q.correct_answer.strip().lower():
                    correct += 1
        attempt.score_raw = correct
        attempt.band_score = round((correct / max(total, 1)) * 9 * 2) / 2
        attempt.save()
        request.user.add_xp(50)
        return redirect('listening:results', attempt_pk=attempt.pk)
    return redirect('listening:list')


@login_required
def results(request, attempt_pk):
    attempt = get_object_or_404(ListeningAttempt, pk=attempt_pk, user=request.user)
    return render(request, 'listening/results.html', {'attempt': attempt})
