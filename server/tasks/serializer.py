from rest_framework import serializers
from . import task
from .redisqueue import RedisQueue
from django.conf import settings
from rq.job import Job, JobStatus


STATUSES = [JobStatus.QUEUED, JobStatus.FINISHED, JobStatus.FAILED,  JobStatus.STARTED, JobStatus.DEFERRED]

redish = RedisQueue(settings.REDIS_URL)

class TaskSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    json_data = serializers.CharField()
    result = serializers.CharField(read_only=True,)
    status = serializers.ChoiceField(choices=STATUSES,read_only=True, default=JobStatus.QUEUED)


    def create(self, validated_data):
        print(validated_data)
        task = redish.enqueue(validated_data)
        return task

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance