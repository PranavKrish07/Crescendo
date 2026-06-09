from rest_framework import serializers
from .models import Quest, SubTask

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'description', 'is_completed']

class QuestSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quest
        fields = ['id', 'title', 'description', 'stat', 'deadline', 'is_daily', 'status', 'difficulty', 'created_at', 'subtasks']
        read_only_fields = ['is_daily', 'status', 'difficulty', 'created_at']
