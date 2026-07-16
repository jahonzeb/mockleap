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
    passages = test.passages.all()
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
        answers = {}
        for key, value in request.POST.items():
            if key.startswith('q') and key[1:].isdigit():
                answers[key[1:]] = value.strip()
        attempt.answers = answers
        attempt.status = 'completed'
        attempt.submitted_at = timezone.now()
        
        correct = 0
        total = 0
        for passage in attempt.test.passages.all():
            if passage.answer_key:
                for q_num, correct_ans in passage.answer_key.items():
                    total += 1
                    given = answers.get(str(q_num), '').lower()
                    if given == str(correct_ans).strip().lower():
                        correct += 1
                        
        attempt.score_raw = correct
        pct = correct / max(total, 1)
        attempt.band_score = round(pct * 9 * 2) / 2
        attempt.save()
        request.user.add_xp(50)
        return redirect('reading:results', attempt_pk=attempt.pk)
    return redirect('reading:list')


@login_required
def results(request, attempt_pk):
    attempt = get_object_or_404(ReadingAttempt, pk=attempt_pk, user=request.user)
    
    questions_data = []
    for passage in attempt.test.passages.all():
        if passage.answer_key:
            # Sort keys numerically if possible
            keys = sorted(passage.answer_key.keys(), key=lambda x: int(x) if x.isdigit() else x)
            for q_num in keys:
                correct_ans = passage.answer_key[q_num]
                given = attempt.answers.get(str(q_num), '')
                is_correct = (given.strip().lower() == str(correct_ans).strip().lower())
                questions_data.append({
                    'number': q_num,
                    'text': '', # No longer storing question text separately
                    'given': given,
                    'correct': correct_ans,
                    'is_correct': is_correct,
                })
                
    return render(request, 'reading/results.html', {
        'attempt': attempt,
        'questions_data': questions_data
    })


from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

@user_passes_test(lambda u: u.is_superuser)
def quick_edit(request, pk):
    test = get_object_or_404(ReadingTest, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            test.title = title
            test.save()
            messages.success(request, f"Test '{test.title}' updated.")
    return redirect('reading:list')

@user_passes_test(lambda u: u.is_superuser)
def delete_test(request, pk):
    test = get_object_or_404(ReadingTest, pk=pk)
    if request.method == 'POST':
        test.delete()
        messages.success(request, "Test deleted successfully.")
    return redirect('reading:list')

@user_passes_test(lambda u: u.is_superuser)
def export_test_json(request, pk):
    test = get_object_or_404(ReadingTest, pk=pk)
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
    response = HttpResponse(json.dumps([test_data], indent=2), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="reading_test_{test.pk}_{test.title[:20].replace(" ", "_")}.json"'
    return response

