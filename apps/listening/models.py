from django.db import models
from django.conf import settings


class ListeningTest(models.Model):
    title = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField(default=40)
    audio_file = models.FileField(upload_to='listening/audio/', null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ListeningSection(models.Model):
    test = models.ForeignKey(ListeningTest, on_delete=models.CASCADE, related_name='sections')
    order = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=200)
    transcript = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.test.title} — Section {self.order}'


class ListeningQuestion(models.Model):
    TYPE_FILL  = 'fill'
    TYPE_MCQ   = 'mcq'
    TYPE_TABLE = 'table'
    TYPE_NOTE  = 'note'
    TYPE_MATCH = 'match'
    TYPE_CHOICES = [
        (TYPE_FILL,  'Form / Sentence Completion'),
        (TYPE_TABLE, 'Table Completion'),
        (TYPE_NOTE,  'Note Completion'),
        (TYPE_MCQ,   'Multiple Choice'),
        (TYPE_MATCH, 'Matching'),
    ]

    section = models.ForeignKey(ListeningSection, on_delete=models.CASCADE, related_name='questions')
    number = models.PositiveSmallIntegerField()
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_FILL)
    option_a = models.CharField(max_length=300, blank=True)
    option_b = models.CharField(max_length=300, blank=True)
    option_c = models.CharField(max_length=300, blank=True)
    option_d = models.CharField(max_length=300, blank=True)
    correct_answer = models.CharField(max_length=200)

    class Meta:
        ordering = ['number']

    @property
    def choices(self):
        result = []
        for letter, text in [('A', self.option_a), ('B', self.option_b), ('C', self.option_c), ('D', self.option_d)]:
            if text:
                result.append((letter, text))
        return result


class ListeningAttempt(models.Model):
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_SUBMITTED = 'submitted'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listening_attempts')
    test = models.ForeignKey(ListeningTest, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, default=STATUS_IN_PROGRESS)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    answers = models.JSONField(default=dict)
    score_raw = models.PositiveSmallIntegerField(null=True, blank=True)
    band_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    class Meta:
        ordering = ['-started_at']
