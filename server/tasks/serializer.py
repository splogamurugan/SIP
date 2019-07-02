from rest_framework import serializers
from . import task

STATUSES = ['New', 'Processing', 'Done']
class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.StringRelatedField()
    status = serializers.ChoiceField(choices=STATUSES, default='New')

    def create(self, validated_data):
        return task.Task(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance