import base64
import io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.base import ContentFile
from .models import SpeakingTest, SpeakingPart, SpeakingSubmission


@login_required
def test_list(request):
    tests = SpeakingTest.objects.filter(is_published=True).prefetch_related('parts')
    submissions = SpeakingSubmission.objects.filter(user=request.user).select_related('part__test')
    return render(request, 'speaking/list.html', {'tests': tests, 'submissions': submissions})


@login_required
def take_test(request, part_pk):
    part = get_object_or_404(SpeakingPart, pk=part_pk, test__is_published=True)
    return render(request, 'speaking/exam.html', {'part': part})


@login_required
def submit_recording(request, part_pk):
    """Handle form POST with base64 audio_data."""
    if request.method == 'POST':
        part = get_object_or_404(SpeakingPart, pk=part_pk)
        audio_data = request.POST.get('audio_data', '')
        duration = int(request.POST.get('duration', 0))
        audio_file = None
        if audio_data and ',' in audio_data:
            _, b64 = audio_data.split(',', 1)
            audio_bytes = base64.b64decode(b64)
            audio_file = ContentFile(audio_bytes, name=f'speaking_{part_pk}_{request.user.pk}.webm')
        submission = SpeakingSubmission.objects.create(
            user=request.user,
            part=part,
            duration_seconds=duration,
        )
        if audio_file:
            submission.audio_file.save(audio_file.name, audio_file, save=True)
        request.user.add_xp(40)
        return redirect('speaking:detail', submission_pk=submission.pk)
    return redirect('speaking:list')


@login_required
def upload_recording(request, part_pk):
    """Handle file upload (API/AJAX usage)."""
    if request.method == 'POST' and request.FILES.get('audio'):
        part = get_object_or_404(SpeakingPart, pk=part_pk)
        submission = SpeakingSubmission.objects.create(
            user=request.user,
            part=part,
            audio_file=request.FILES['audio'],
            duration_seconds=int(request.POST.get('duration', 0)),
        )
        request.user.add_xp(40)
        return HttpResponse('')
    return HttpResponse('Error', status=400)


@login_required
def submission_detail(request, submission_pk):
    submission = get_object_or_404(SpeakingSubmission, pk=submission_pk, user=request.user)
    return render(request, 'speaking/submission_detail.html', {'submission': submission})
