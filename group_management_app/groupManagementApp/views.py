from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Q
from django.contrib.auth import login

from .forms import ProjectForm, TaskForm
from .models import Project, Task
from .forms import CustomUserCreationForm
from django.utils import timezone


@login_required
def home(request):
    now = timezone.now()
    projects = user_projects(request.user)

    closest_projects = (
        projects.filter(completed=False, due_date__gte=now)
        .select_related("owner")
        .prefetch_related(
            "contributors",
            Prefetch("tasks", queryset=Task.objects.order_by("due_date")),
        )
        .order_by("due_date")[:5]
    )
    closest_tasks = (
        Task.objects.filter(project__in=projects, completed=False, due_date__gte=now)
        .order_by("due_date")[:10]
    )
    return render(request, "home/home.html", {
        "closest_projects": closest_projects,
        "closest_tasks": closest_tasks,
    })

def dashboard(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "registration/dashboard.html")

def sign_up(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/sign_up.html', {'form': form})


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
