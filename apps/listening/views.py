from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import ListeningTest, ListeningAttempt
import urllib.request
from django.http import StreamingHttpResponse, Http404

def stream_audio(request, file_id):
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        def generate():
            while True:
                chunk = response.read(8192)
                if not chunk:
                    break
                yield chunk
        res = StreamingHttpResponse(generate(), content_type=response.getheader('Content-Type', 'audio/mpeg'))
        res['Content-Disposition'] = f'inline; filename="audio.mp3"'
        res['Accept-Ranges'] = 'bytes'
        return res
    except Exception as e:
        raise Http404("Audio file not found or inaccessible")


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
        answers = {}
        for key, value in request.POST.items():
            if key.startswith('q') and key[1:].isdigit():
                answers[key[1:]] = value.strip()
        attempt.answers = answers
        attempt.status = 'completed'
        attempt.submitted_at = timezone.now()
        
        correct = 0
        total = 0
        for sec in attempt.test.sections.all():
            if sec.answer_key:
                for q_num, correct_ans in sec.answer_key.items():
                    total += 1
                    given = answers.get(str(q_num), '').lower()
                    if given == str(correct_ans).strip().lower():
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
    
    questions_data = []
    for sec in attempt.test.sections.all():
        if sec.answer_key:
            keys = sorted(sec.answer_key.keys(), key=lambda x: int(x) if x.isdigit() else x)
            for q_num in keys:
                correct_ans = sec.answer_key[q_num]
                given = attempt.answers.get(str(q_num), '')
                is_correct = (given.strip().lower() == str(correct_ans).strip().lower())
                questions_data.append({
                    'number': q_num,
                    'text': '',
                    'given': given,
                    'correct': correct_ans,
                    'is_correct': is_correct,
                })
                
    return render(request, 'listening/results.html', {
        'attempt': attempt,
        'questions_data': questions_data
    })


from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

@user_passes_test(lambda u: u.is_superuser)
def quick_edit(request, pk):
    test = get_object_or_404(ListeningTest, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        audio_url = request.POST.get('audio_url')
        if title:
            test.title = title
            test.audio_url = audio_url
            test.save()
            messages.success(request, f"Test '{test.title}' updated.")
    return redirect('listening:list')

@user_passes_test(lambda u: u.is_superuser)
def delete_test(request, pk):
    test = get_object_or_404(ListeningTest, pk=pk)
    if request.method == 'POST':
        test.delete()
        messages.success(request, "Test deleted successfully.")
    return redirect('listening:list')

import json
from django.http import HttpResponse

@user_passes_test(lambda u: u.is_superuser)
def export_test_json(request, pk):
    test = get_object_or_404(ListeningTest, pk=pk)
    test_data = {
        'title': test.title,
        'duration_minutes': test.duration_minutes,
        'audio_url': test.audio_url,
        'is_published': test.is_published,
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
    response = HttpResponse(json.dumps([test_data], indent=2), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="listening_test_{test.pk}_{test.title[:20].replace(" ", "_")}.json"'
    return response

