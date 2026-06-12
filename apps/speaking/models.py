from django.db import models
from django.conf import settings


class SpeakingTest(models.Model):
    title = models.CharField(max_length=200)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SpeakingPart(models.Model):
    PART1 = 'part1'
    PART2 = 'part2'
    PART3 = 'part3'
    PART_CHOICES = [(PART1, 'Part 1'), (PART2, 'Part 2'), (PART3, 'Part 3')]

    test = models.ForeignKey(SpeakingTest, on_delete=models.CASCADE, related_name='parts')
    part_type = models.CharField(max_length=5, choices=PART_CHOICES)
    order = models.PositiveSmallIntegerField(default=1)
    prompt = models.TextField()
    prep_time_seconds = models.PositiveSmallIntegerField(default=60)
    speak_time_seconds = models.PositiveSmallIntegerField(default=120)
    cue_card_points = models.TextField(blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.test.title} — {self.get_part_type_display()}'

    @property
    def cue_card_points_list(self):
        if not self.cue_card_points:
            return []
        return [line.strip() for line in self.cue_card_points.splitlines() if line.strip()]


class SpeakingSubmission(models.Model):
    STATUS_SUBMITTED = 'submitted'
    STATUS_REVIEWED = 'reviewed'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='speaking_submissions')
    part = models.ForeignKey(SpeakingPart, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='speaking/recordings/', null=True, blank=True)
    duration_seconds = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(max_length=10, default=STATUS_SUBMITTED)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Teacher review
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='speaking_reviews')
    band_fluency = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    band_lexical = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    band_grammar = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    band_pronunciation = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    overall_band = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    teacher_comment = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-submitted_at']
