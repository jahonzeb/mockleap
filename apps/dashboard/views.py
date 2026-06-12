from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.reading.models import ReadingAttempt
from apps.listening.models import ListeningAttempt
from apps.writing.models import WritingSubmission
from apps.speaking.models import SpeakingSubmission


@login_required
def home(request):
    user = request.user
    reading_attempts = ReadingAttempt.objects.filter(
        user=user, status='submitted'
    ).select_related('test').order_by('-submitted_at')[:5]
    listening_attempts = ListeningAttempt.objects.filter(
        user=user, status='submitted'
    ).select_related('test').order_by('-submitted_at')[:5]
    writing_subs = WritingSubmission.objects.filter(
        user=user
    ).exclude(status='draft').select_related('task__test').order_by('-created_at')[:5]
    speaking_subs = SpeakingSubmission.objects.filter(
        user=user
    ).select_related('part__test').order_by('-submitted_at')[:5]

    # Compute skill averages
    def avg(qs, field):
        vals = [getattr(a, field) for a in qs if getattr(a, field) is not None]
        return round(sum(float(v) for v in vals) / len(vals), 1) if vals else None

    reading_avg = avg(reading_attempts, 'band_score')
    listening_avg = avg(listening_attempts, 'band_score')
    writing_avg = avg(writing_subs, 'overall_band')
    speaking_avg = avg(speaking_subs, 'overall_band')

    context = {
        'reading_attempts': reading_attempts,
        'listening_attempts': listening_attempts,
        'writing_subs': writing_subs,
        'speaking_subs': speaking_subs,
        'reading_avg': reading_avg,
        'listening_avg': listening_avg,
        'writing_avg': writing_avg,
        'speaking_avg': speaking_avg,
        'total_tests': reading_attempts.count() + listening_attempts.count(),
        'total_writing': writing_subs.count(),
        'total_speaking': speaking_subs.count(),
    }
    return render(request, 'dashboard/home.html', context)
