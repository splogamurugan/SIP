import redis
from rq import Queue, Connection, Worker, cancel_job, registry, requeue_job
from . import processor
from rq.job import Job, JobStatus
from rq.registry import (DeferredJobRegistry, FailedJobRegistry,
                         FinishedJobRegistry, StartedJobRegistry)
from rq.exceptions import NoSuchJobError, InvalidJobOperation

class RedisQueue():
    conn = None

    def __init__(self, url:str):
        self.url = url

    def __getdata(self, task):
        return {
            'id': task.get_id(),
            'status': task.get_status(),
            'result': task.result,
            'json_data': str(task.kwargs)
        }


    def enqueue(self, content:dict):
        with Connection(redis.from_url(self.url)):
            q = Queue()
            task = q.enqueue(processor.processor, kwargs=content)
        return {
            'status': 'success',
            'data': self.__getdata(task)
        }
    
    def retrieve(self, task_id):
        with Connection(redis.from_url(self.url)):
            q = Queue()
            task = q.fetch_job(task_id)
        
        if task:
            return {
                'status': 'success',
                'data': self.__getdata(task)
            }
        else:
            return {
                'status': 'error'
            }
    
    def clear(self):
        with Connection(redis.from_url(self.url)):
            q = Queue()
            q.empty()
    
    def worker(self):
        redish = redis.from_url(self.url)
        with Connection(redish):
            worker = Worker(['default'])
            worker.work()
        
    def queued_jobs(self):
        jobs = []
        with Connection(redis.from_url(self.url)):
            q = Queue()
            job_ids =  q.get_job_ids()
            for job_id in job_ids:
                try:
                    jobs.append(self.__getdata(Job.fetch(job_id)))
                except NoSuchJobError:
                    pass
        return jobs
        
    def __jobs(self, registry_type:str='FinishedJobRegistry'):
        jobs = []
        with Connection(redis.from_url(self.url)):
            class_ = getattr(registry, registry_type)
            reg = class_()
            job_ids = reg.get_job_ids()
            
            for job_id in job_ids:
                try:
                    jobs.append(self.__getdata(Job.fetch(job_id)))
                except NoSuchJobError:
                    pass
        return jobs

    def finished_jobs(self):
        return self.__jobs('FinishedJobRegistry')
    
    def failed_jobs(self):
        return self.__jobs('FailedJobRegistry')
    
    def started_jobs(self):
        return self.__jobs('StartedJobRegistry')
    
    def deferred_jobs(self):
        return self.__jobs('DeferredJobRegistry')

    def cancel(self, task_id):
        with Connection(redis.from_url(self.url)):
            cancel_job(task_id)

    def delete(self, task_id):
        res = {'status':'success'}
        with Connection(redis.from_url(self.url)):
            try:
                job = Job.fetch(task_id)
                job.delete()
            except NoSuchJobError:
                res = {'status':'error'}
                pass
        return res

    def requeue_all(self):
        with Connection(redis.from_url(self.url)):
            q = Queue()
            reg = FailedJobRegistry()
            tasks = reg.get_job_ids()
            for task in tasks:
                print(task)
                requeue_job(task, q.connection)

    def requeue(self, task_id):
        with Connection(redis.from_url(self.url)):
            try:
                q = Queue()
                task = Job.fetch(task_id)
                requeue_job(task_id, q.connection)
                return {
                    'status': 'success',
                    'data': self.__getdata(task)
                }
            except NoSuchJobError:
                pass
            except InvalidJobOperation:
                pass
            
        return {
            'status': 'error',
        }

    def update(self, task_id):

        pass
    
    def workers(self):
        all_workers = []
        with Connection(redis.from_url(self.url)):
            all_workers = Worker.all()
            all_workers = [ {"name": worker.name} for worker in all_workers]
        return {
            "data": all_workers
        }