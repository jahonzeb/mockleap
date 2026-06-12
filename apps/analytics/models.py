from django.db import models
from django.conf import settings


class DailyActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_activities')
    date = models.DateField()
    listening_minutes = models.PositiveSmallIntegerField(default=0)
    reading_minutes = models.PositiveSmallIntegerField(default=0)
    writing_minutes = models.PositiveSmallIntegerField(default=0)
    speaking_minutes = models.PositiveSmallIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    @property
    def total_minutes(self):
        return self.listening_minutes + self.reading_minutes + self.writing_minutes + self.speaking_minutes
