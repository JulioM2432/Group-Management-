from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('projects/', views.projects, name='projects'),
    path('projects/add_project', views.add_project, name='add_project'),
    path('projects/<int:project_id>', views.project_view, name='project_view'),
    path('projects/<int:project_id>/add_task', views.add_task, name='add_task'),
]
