from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(
            owner=self.request.user
        ).prefetch_related('tasks')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(
            project__owner=self.request.user
        ).select_related('project')

    # GET /api/tasks/overdue/
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        today = timezone.now().date()
        tasks = self.get_queryset().filter(
            deadline__lt=today
        ).exclude(status='completed')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    # GET /api/tasks/by-deadline/?date=YYYY-MM-DD
    @action(detail=False, methods=['get'], url_path='by-deadline')
    def by_deadline(self, request):
        date_param = request.query_params.get('date')
        if not date_param:
            return Response(
                {"error": "Please provide ?date=YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            tasks = self.get_queryset().filter(deadline=date_param)
            serializer = self.get_serializer(tasks, many=True)
            return Response(serializer.data)
        except Exception:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

    # GET /api/tasks/by-priority/?level=high
    @action(detail=False, methods=['get'], url_path='by-priority')
    def by_priority(self, request):
        level = request.query_params.get('level')
        if level not in ['low', 'medium', 'high']:
            return Response(
                {"error": "level must be low, medium, or high"},
                status=status.HTTP_400_BAD_REQUEST
            )
        tasks = self.get_queryset().filter(priority=level)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)