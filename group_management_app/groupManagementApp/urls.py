from django.urls import path, include
from django.contrib.auth import views as auth_views
from .forms import StyledPasswordResetForm, StyledSetPasswordForm
from . import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', views.home, name='home'),
    path('', views.dashboard, name='dashboard'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('projects/', views.projects, name='projects'),
    path('projects/add_project', views.add_project, name='add_project'),
    path('projects/<int:project_id>', views.project_view, name='project_view'),
    path('projects/<int:project_id>/add_task', views.add_task, name='add_task'),
    #account reset password
    path("password_reset/", auth_views.PasswordResetView.as_view(form_class=StyledPasswordResetForm), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(form_class=StyledSetPasswordForm), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]
