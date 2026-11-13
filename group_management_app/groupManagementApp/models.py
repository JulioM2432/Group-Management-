from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_projects")
    contributors = models.ManyToManyField(User, related_name="projects", blank=True)

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(User, related_name="tasks", blank=True)

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
