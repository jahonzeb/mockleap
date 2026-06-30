from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_STUDENT = 'student'
    ROLE_TEACHER = 'teacher'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_STUDENT, 'Student'),
        (ROLE_TEACHER, 'Teacher'),
        (ROLE_ADMIN, 'Admin'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_STUDENT)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    target_band = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    test_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    dark_mode = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    xp = models.PositiveIntegerField(default=0)
    streak_days = models.PositiveIntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    @property
    def is_student(self):
        return self.role == self.ROLE_STUDENT

    @property
    def is_teacher(self):
        return self.role == self.ROLE_TEACHER or self.is_staff or self.is_superuser

    @property
    def initials(self):
        name = self.get_full_name() or self.username
        parts = name.split()
        return ''.join(p[0] for p in parts[:2]).upper()

    def add_xp(self, amount):
        self.xp += amount
        self.save(update_fields=['xp'])
