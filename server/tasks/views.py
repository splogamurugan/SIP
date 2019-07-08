from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render
from rest_framework import viewsets, status
from . import serializer
from .task import Task
from rest_framework.decorators import api_view
from tasks.redisqueue import RedisQueue
from django.conf import settings

import json
from json.decoder import JSONDecodeError

from importlib import util

import sys
from os import path
sys.path.append(path.join(path.dirname(path.abspath(__file__)), 'jobs'))
import JobsSpecs

class TaskViewSet(viewsets.ViewSet):
    serializer_class = serializer.TaskSerializer
    redisq = RedisQueue(settings.REDIS_URL)    

    def list(self, request):

        tasks = getattr(
            self.redisq, 
            str(request.GET.get('status'))+'_jobs',
            self.redisq.queued_jobs
        )()
        
        ser = serializer.TaskSerializer(
            instance=tasks, 
            many=True
        )
        return Response(ser.data)

    def create(self, request):
        #ser = serializer.TaskSerializer(data=request.POST)
        try:
            arg = request.POST['json_data']
            arg = arg.replace("'", "\"")
            arg = json.loads(arg)
            data = self.redisq.enqueue(arg)
            return Response(data, status=status.HTTP_201_CREATED)
        except JSONDecodeError as e:
            return Response({'status':'error', 'message':e}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response({'status':'error'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            task = self.redisq.retrieve(pk)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(task)

    '''
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
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    '''

    def destroy(self, request, pk=None):
        try:
            task = self.redisq.retrieve(pk)
            self.redisq.delete(pk)
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
@api_view(['PUT', 'POST'])
def bulk(request):
    #print(request.POST['json_data'])

    try:
        arg = request.POST['json_data']
        arg = arg.replace("'", "\"")
        arg = json.loads(arg)

        if type(arg) != list:
            arg = [arg]

        for item in arg:
            #print(item)
            RedisQueue(settings.REDIS_URL).enqueue(item)
        return Response({"status":"success"}, status=status.HTTP_201_CREATED)
    except JSONDecodeError as e:
        return Response({'status':'error', 'message':e}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except TypeError:
        return Response({'status':'error', 'message':"Please give JSON in array format"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def workers(request):
    data = RedisQueue(settings.REDIS_URL).workers()
    return Response(data)

@api_view(['GET'])
def stats(request):
    data = RedisQueue(settings.REDIS_URL).stats()
    return Response(data)

@api_view(['GET'])
def job_handlers(request):
    j = JobsSpecs()
    return Response(j.jobs())

    #return Response(status=status.HTTP_404_NOT_FOUND)

