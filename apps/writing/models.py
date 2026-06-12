from django.db import models
from django.conf import settings


class WritingTest(models.Model):
    title = models.CharField(max_length=200)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class WritingTask(models.Model):
    TASK1 = 'task1'
    TASK2 = 'task2'
    TASK_CHOICES = [(TASK1, 'Task 1'), (TASK2, 'Task 2')]

    test = models.ForeignKey(WritingTest, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.CharField(max_length=5, choices=TASK_CHOICES)
    order = models.PositiveSmallIntegerField(default=1)
    prompt = models.TextField()
    min_words = models.PositiveSmallIntegerField(default=250)
    time_minutes = models.PositiveSmallIntegerField(default=40)
    image = models.ImageField(upload_to='writing/task_images/', null=True, blank=True)

    class Meta:
        ordering = ['order']


class WritingSubmission(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_SUBMITTED = 'submitted'
    STATUS_REVIEWED = 'reviewed'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_REVIEWED, 'Reviewed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='writing_submissions')
    task = models.ForeignKey(WritingTask, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    content = models.TextField()
    word_count = models.PositiveSmallIntegerField(default=0)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Teacher review fields
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='writing_reviews')
    band_task_response = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    band_coherence = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    band_lexical = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    band_grammar = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    overall_band = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    teacher_comment = models.TextField(blank=True)
    corrected_text = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} — {self.task}'

    def compute_overall(self):
        scores = [self.band_task_response, self.band_coherence, self.band_lexical, self.band_grammar]
        valid = [s for s in scores if s is not None]
        if valid:
            self.overall_band = round(sum(float(s) for s in valid) / len(valid) * 2) / 2
