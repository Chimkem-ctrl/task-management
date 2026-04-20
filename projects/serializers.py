from rest_framework import serializers
from django.utils import timezone
from .models import Project, Task


class TaskSerializer(serializers.ModelSerializer):
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'project', 'title', 'description',
            'priority', 'status', 'deadline',
            'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_is_overdue(self, obj):
        return obj.is_overdue

    def validate_deadline(self, value):
        # Deadline validation: must not be in the past on CREATE
        if self.instance is None and value < timezone.now().date():
            raise serializers.ValidationError(
                "Deadline cannot be in the past."
            )
        return value


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    task_count = serializers.SerializerMethodField()
    overdue_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description',
            'task_count', 'overdue_count',
            'tasks', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_task_count(self, obj):
        return obj.tasks.count()

    def get_overdue_count(self, obj):
        today = timezone.now().date()
        return obj.tasks.filter(
            deadline__lt=today
        ).exclude(status='completed').count()