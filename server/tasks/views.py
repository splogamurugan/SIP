from rest_framework.response import Response

from django.shortcuts import render
from rest_framework import viewsets, status
from . import serializer
from .task import Task

tasks = {
    1: Task(id=1, name='Demo', status='Done'),
    2: Task(id=2, name='Model less demo', status='Process'),
    3: Task(id=3, name='Sleep more', status='New'),
}

def get_next_task_id():
    return max(tasks)+1

class TaskViewSet(viewsets.ViewSet):
    serializer_class = serializer.TaskSerializer

    def list(self, request):
        #global serializer
        ser = serializer.TaskSerializer(
            instance=tasks.values(), 
            many=True
        )
        return Response(ser.data)

    def create(self, request):
        ser = serializer.TaskSerializer(data=request.data)
        if ser.is_valid():
            task = ser.save()
            task.id = get_next_task_id()
            tasks[task.id] = task
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            task = tasks[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ser = serializer.TaskSerializer(instance=task)
        return Response(ser.data)
    
    def update(self, request, pk=None):
        try:
            task = tasks[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ser = serializer.TaskSerializer(
            data=request.data, instance=task)
        if ser.is_valid():
            task = ser.save()
            tasks[task.id] = task
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            task = tasks[int(pk)]
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        del tasks[int(pk)]

        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.

def index(request):
    context = {}
    return render(request, 'index.html', context=context)
