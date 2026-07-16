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
    source = models.CharField(max_length=255, blank=True)
    
    questions_html = models.TextField(blank=True, help_text="Raw HTML for the questions section")
    answer_key = models.JSONField(default=dict, help_text="JSON mapping of question numbers to correct answers e.g. {'1': 'A', '2': 'TRUE'}")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Passage {self.order}: {self.title}"

    @property
    def paragraphs(self):
        paras = [p.strip() for p in self.content.split('\n\n') if p.strip()]
        if paras and paras[0].strip() == self.title.strip():
            paras = paras[1:]
        return paras

class ReadingAttempt(models.Model):
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_SUBMITTED = 'completed'
    STATUS_CHOICES = (
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_SUBMITTED, 'Completed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(ReadingTest, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_IN_PROGRESS)
    
    answers = models.JSONField(default=dict)
    score_raw = models.PositiveIntegerField(null=True, blank=True)
    band_score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    def calculate_score(self):
        pass

    def __str__(self):
        return f"{self.user.username} - {self.test.title} ({self.status})"
