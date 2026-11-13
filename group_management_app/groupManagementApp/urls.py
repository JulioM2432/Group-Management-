from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.members, name='members'),
    path('register/', views.sign_up, name='register'),
    path('projects/', views.projects, name='projects'),
    path('projects/add_project', views.add_project, name='add_project'),
    path('projects/<int:project_id>', views.project_view, name='project_view'),
    path('projects/<int:project_id>/add_task', views.add_task, name='add_task'),
]
