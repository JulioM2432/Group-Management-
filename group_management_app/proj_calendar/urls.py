from django.urls import path
from . import views

urlpatterns = [
    path(
        'calendar/',
        views.CalendarEventListView.as_view(),
        name='calendar-events'

    ),
    path(
        'calendar/<int:pk>/',
        views.CalendarEventDetailView.as_view(),
        name='calendar-event-detail'
    ),
]