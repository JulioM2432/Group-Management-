from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProjectForm
from .models import Project


def members(request):
    return render(request, "home.html")


@login_required
def add_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        return redirect("project_view", project_id=project.pk)
    return render(request, "project/add_project.html", {"form": form})


def user_projects(user):
    return Project.objects.filter(Q(owner=user) | Q(contributors=user)).distinct()


@login_required
def projects(request):
    return render(request, "project/project_list.html",
                  {"projects": user_projects(request.user)})


@login_required
def project_view(request, project_id):
    project = get_object_or_404(user_projects(request.user), pk=project_id)
    return render(request, "project/view_project.html", {
        "project": project,
        "tasks": project.tasks.all(),
        "contributors": project.contributors.all(),
    })
