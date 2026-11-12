from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.members, name='members'),
    path('register/', views.sign_up, name='register'),
]