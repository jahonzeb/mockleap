from django.db import models
from django.conf import settings

import re

class ListeningTest(models.Model):
    title = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField(default=40)
    audio_file = models.FileField(upload_to='listening/audio/', null=True, blank=True)
    audio_url = models.URLField(max_length=500, null=True, blank=True, help_text="Direct link to audio, or Google Drive link")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_audio_src(self):
        if self.audio_url:
            if 'drive.google.com' in self.audio_url:
                match = re.search(r'/d/([^/]+)/', self.audio_url)
                if match:
                    return f"/listening/proxy/{match.group(1)}/"
                match = re.search(r'id=([^&]+)', self.audio_url)
                if match:
                    return f"/listening/proxy/{match.group(1)}/"
            return self.audio_url
        if self.audio_file:
            return self.audio_file.url
        return None

    def __str__(self):
        return self.title

class ListeningSection(models.Model):
    test = models.ForeignKey(ListeningTest, on_delete=models.CASCADE, related_name='sections')
    order = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=200)
    transcript = models.TextField(blank=True)
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='listening/sections/', null=True, blank=True)
    
    questions_html = models.TextField(blank=True, help_text="Raw HTML for the questions section")
    answer_key = models.JSONField(default=dict, help_text="JSON mapping of question numbers to correct answers e.g. {'1': 'A', '2': 'apple'}")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Section {self.order}: {self.title}"

class ListeningAttempt(models.Model):
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_SUBMITTED = 'completed'
    STATUS_CHOICES = (
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_SUBMITTED, 'Completed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(ListeningTest, on_delete=models.CASCADE)
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
