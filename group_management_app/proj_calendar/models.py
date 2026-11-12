from django.db import models
from django.conf import settings


# Create your models here.
class CalendarEvents(models.Model):
    # I feel like there should be two calendar types, a personal and a shared one
    VISIBILITY_CHOICES = [
        ('personal', 'Personal'),
        ('shared', 'Shared')
    ]

    title = models.CharField(max_length=200) 
    description = models.TextField(blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    visibility = models.CharField(
        max_length=10,
        choices=VISIBILITY_CHOICES,
        default='personal'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name='calendar_events'
    )

    def __str__(self):
        return self.title


