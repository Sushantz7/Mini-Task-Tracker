from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from utils.base_model import BaseModel



class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Task(BaseModel):
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    PRIORITY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=255, unique=True)
    start_date = models.DateField()
    est_end_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    numeric_target = models.FloatField()
    numeric_current = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="medium"
    )
    notes = models.TextField(blank=True)

    def progress_percentage(self):
        return (
            (self.numeric_current / self.numeric_target) * 100
            if self.numeric_target
            else 0
        )

    def save(self, *args, **kwargs):
        if self.numeric_current > self.numeric_target:
            self.numeric_current = self.numeric_target
        super().save(*args, **kwargs)

    def __str__(self):
        return self.task_name


class AuditLog(BaseModel):
    ACTION_CHOICES = [
        ("create", "Created"),
        ("update", "Updated"),
        ("delete", "Deleted"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} {self.action} {self.task.task_name if self.task else 'task'} at {self.timestamp}"
