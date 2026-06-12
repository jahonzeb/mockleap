from django.db import models
from django.conf import settings


class ReadingTest(models.Model):
    TYPE_ACADEMIC = 'academic'
    TYPE_GENERAL = 'general'
    TYPE_CHOICES = [(TYPE_ACADEMIC, 'Academic'), (TYPE_GENERAL, 'General Training')]

    title = models.CharField(max_length=200)
    test_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_ACADEMIC)
    duration_minutes = models.PositiveIntegerField(default=60)
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reading_tests_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ReadingPassage(models.Model):
    test = models.ForeignKey(ReadingTest, on_delete=models.CASCADE, related_name='passages')
    order = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=300)
    content = models.TextField()
    source = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.test.title} — Passage {self.order}'

    @property
    def paragraphs(self):
        paras = [p.strip() for p in self.content.split('\n\n') if p.strip()]
        # Skip leading paragraph if it duplicates the title field
        if paras and paras[0].strip() == self.title.strip():
            paras = paras[1:]
        return paras


class QuestionGroup(models.Model):
    TYPE_MCQ     = 'mcq'
    TYPE_TFNG    = 'tfng'
    TYPE_FILL    = 'fill'
    TYPE_TABLE   = 'table'
    TYPE_NOTE    = 'note'
    TYPE_SUMMARY = 'summary'
    TYPE_MATCH   = 'match'
    TYPE_SHORT   = 'short'
    TYPE_CHOICES = [
        (TYPE_MCQ,     'Multiple Choice'),
        (TYPE_TFNG,    'True / False / Not Given'),
        (TYPE_FILL,    'Fill in the Blank'),
        (TYPE_TABLE,   'Table Completion'),
        (TYPE_NOTE,    'Note Completion'),
        (TYPE_SUMMARY, 'Summary Completion'),
        (TYPE_MATCH,   'Matching Headings'),
        (TYPE_SHORT,   'Short Answer'),
    ]
    passage = models.ForeignKey(ReadingPassage, on_delete=models.CASCADE, related_name='question_groups')
    question_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    instructions = models.TextField()
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['order']


class Question(models.Model):
    group = models.ForeignKey(QuestionGroup, on_delete=models.CASCADE, related_name='questions')
    number = models.PositiveSmallIntegerField()
    text = models.TextField()
    option_a = models.CharField(max_length=500, blank=True)
    option_b = models.CharField(max_length=500, blank=True)
    option_c = models.CharField(max_length=500, blank=True)
    option_d = models.CharField(max_length=500, blank=True)
    correct_answer = models.CharField(max_length=200)
    explanation = models.TextField(blank=True)

    class Meta:
        ordering = ['number']

    @property
    def choices(self):
        result = []
        for letter, text in [('A', self.option_a), ('B', self.option_b), ('C', self.option_c), ('D', self.option_d)]:
            if text:
                result.append((letter, text))
        return result


class ReadingAttempt(models.Model):
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_SUBMITTED = 'submitted'
    STATUS_CHOICES = [(STATUS_IN_PROGRESS, 'In Progress'), (STATUS_SUBMITTED, 'Submitted')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reading_attempts')
    test = models.ForeignKey(ReadingTest, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    time_taken_seconds = models.PositiveIntegerField(default=0)
    score_raw = models.PositiveSmallIntegerField(null=True, blank=True)
    band_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    answers = models.JSONField(default=dict)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f'{self.user.email} — {self.test.title}'
