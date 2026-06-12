from django.db import models

class SiteSettings(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    class Meta:
        verbose_name_plural = 'Site Settings'
    def __str__(self):
        return self.key
