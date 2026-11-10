from .models import Project, Task
from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "due_date"]   # completed defaults to False
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "due_date": forms.DateTimeInput(
                attrs={"type": "datetime-local",
                       "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "assignees"] # completed defaults to False
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "due_date": forms.DateTimeInput(
                attrs={"type": "datetime-local",
                       "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "assignees": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        if project is not None:
            # Filter for Project Members only
            self.fields["assignees"].queryset = User.objects.filter(
                # Is owner of project or project in user projects
                Q(pk=project.owner_id) | Q(projects=project)
            ).distinct()

