from rest_framework import serializers
from .models import Project, Task

class TaskSerializer(serializers.ModelSerializer):
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'description',
                  'priority', 'deadline', 'is_completed',
                  'is_overdue', 'created_at']

    def get_is_overdue(self, obj):
        return obj.is_overdue()

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'tasks', 'created_at']