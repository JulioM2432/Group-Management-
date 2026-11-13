# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

GProj — a Django group-management app for student collaboration on group
projects. CSCI-3340 team project, 3 contributors. Django 6.0.8, Python 3.13,
SQLite, server-rendered templates with Bootstrap via CDN. No JS build, no API.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full design.

## Commands

Dependencies come from a **Nix dev shell**, not pip — there is no
`requirements.txt` or virtualenv. direnv enters it automatically; if
`import django` fails, the shell isn't active (`direnv allow`, or `nix develop`).

`manage.py` lives inside `group_management_app/`, but commands are run from the
repo root with that prefix (matching the `Makefile`):

```bash
make run                                                  # runserver on :8000
python group_management_app/manage.py migrate
python group_management_app/manage.py makemigrations
python group_management_app/manage.py createsuperuser
python group_management_app/manage.py check
```

## Directory layout warning

Three similarly named directories — check which one you're editing:

- `group_management_app/` — outer Django **project** dir, holds `manage.py`
- `group_management_app/group_management_app/` — **settings** package
  (`settings.py`, root `urls.py`, `wsgi.py`)
- `group_management_app/groupManagementApp/` — the **app**, camelCase; all
  models, views, forms, and templates live here

**There are two `urls.py` files.** New routes go in the app one
(`groupManagementApp/urls.py`); the root one only mounts the app and `/admin/`.

## Conventions

- **Scope project lookups through `user_projects()`.** In `views.py`, resolve a
  project with `get_object_or_404(user_projects(request.user), pk=project_id)` —
  never `Project.objects.get(pk=...)` followed by an ownership `if`. Filtering
  the queryset is what makes non-members get a 404 and keeps the check
  impossible to forget. Reuse this helper in every new project-scoped view.
- **Always pass `project=` to `TaskForm`.** It narrows the `assignees` queryset
  to project members, which Django enforces at validation time. Omitting it
  silently allows assigning any user.
- **Bootstrap classes belong in form `Meta.widgets`**, not hardcoded in
  templates — that's why templates can loop generically over fields.
- **Templates** extend `home/base.html` and fill `{% block content %}`. Forms
  loop `{% for field in form %}` and must include `{% csrf_token %}`.
- **A new page = URL name + view + template.** Link to it with
  `{% url 'name' %}`, never a hardcoded path.
- After editing `models.py`, run `makemigrations` and **commit the migration**.

## Version control

- **Never commit:** `db.sqlite3`, `__pycache__/`, `*.pyc` — all gitignored.
  Each contributor builds their own database with `migrate`.
- **Do commit:** migrations, so all three contributors share one schema history.
- Don't change `DEBUG`, `SECRET_KEY`, or the Nix flake pins unless asked.

## Testing and verification

Run the tests with `python group_management_app/manage.py test groupManagementApp`.
They cover project access control and task-assignee restrictions. Coverage is
otherwise thin, so also exercise pages in the browser for anything view- or
template-related.

**Authentication is not implemented yet.** `@login_required` is applied to four
views, but no login route exists (`/accounts/login/` 404s). Don't assume a
working login flow: create a superuser, sign in at `/admin/`, and reuse that
session to reach `/projects/`. `/admin/` is also the only way to add project
contributors or mark things completed.

The site root `/` is unrouted and 404s — the entry point is `/home/`.
