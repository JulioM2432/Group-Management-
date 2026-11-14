from rest_framework import serializers
from .models import CalendarEvents

class CalendarEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = CalendarEvents
        fields = [
            'id',
            'title',
            'description',
            'start_time',
            'end_time',
            'visibility',
            'created_by'
        ]

        read_only_fields = ['id', 'created_by']