from django.template import loader
from django.shortcuts import render, redirect   
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import LoginForm, ProjectForm, TaskForm
from .models import Project


def home(request):
    return render(request, "home/home.html")


### Sign-in, Sign-out, Sign-up
def sign_in(request):
    if request.method == "GET":
        form = LoginForm(request.GET)


def sign_up(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def user_projects(user):
    return Project.objects.filter(Q(owner=user) | Q(contributors=user)).distinct()


@login_required
def add_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        return redirect("project_view", project_id=project.pk)
    return render(request, "project/add_project.html", {"form": form})


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

@login_required
def add_task(request, project_id):
    project = get_object_or_404(user_projects(request.user), pk=project_id)

    form = TaskForm(request.POST or None, project=project)
    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m() # Saves Assigneees (ManyToManyField)
        return redirect("project_view", project_id=project.pk)
    return render(request, "project/tasks/add_task.html", {"form": form, "project": project})
