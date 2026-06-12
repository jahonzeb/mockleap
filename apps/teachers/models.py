from django.db import models
from django.conf import settings


class TeacherProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    bio = models.TextField(blank=True)
    specializations = models.CharField(max_length=200, blank=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Teacher: {self.user.email}'
