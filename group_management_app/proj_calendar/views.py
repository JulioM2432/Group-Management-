from rest_framework import generics, permissions
from .models import CalendarEvents
from .serializers import CalendarEventSerializer


class CalendarEventListView(generics.ListCreateAPIView):


    serializer_class = CalendarEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CalendarEvents.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class CalendarEventDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = CalendarEventSerializer
    permission_classes =  [permissions.IsAuthenticated]

    def get_queryset(self):
        return CalendarEvents.objects.filter(created_by=self.request.user)