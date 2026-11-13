from django.contrib import admin

# Register your models here.
from .models import Task, Project
admin.site.register(Task)
admin.site.register(Project)
