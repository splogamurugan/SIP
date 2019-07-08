import redis
from rq import Queue, Connection, Worker, cancel_job, registry, requeue_job
from . import processor
from rq.job import Job, JobStatus
from rq.registry import (DeferredJobRegistry, FailedJobRegistry,
                         FinishedJobRegistry, StartedJobRegistry)
from rq.exceptions import NoSuchJobError, InvalidJobOperation
from random import randint



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


    def enqueue(self, job_handler, content:dict):
        with Connection(redis.from_url(self.url)):
            q = Queue()
            arguments = {}
            arguments['job_handler'] = job_handler
            arguments['arguments'] = content
            task = q.enqueue(processor.processor, kwargs=arguments)
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
    
    def active_jobs(self):
        return (self.started_jobs() + self.queued_jobs())
        
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
    
    def testing_bulk_add(self, nums):
        for _ in range(int(nums)):
            self.enqueue({"id": randint(0, 3000)})
        return {
            'status': f'{nums} of items have been added to the queue'
        }

    def update(self, task_id):

        pass
    
    def workers(self):
        all_workers = []
        def fmt(spec):
            return 'N/A'

        with Connection(redis.from_url(self.url)):
            all_workers = Worker.all()
            all_workers = [ {"name": worker.name, "state": worker.get_state(), "birth_date": getattr(worker.birth_date, 'strftime', fmt)("%Y-%m-%d %H:%M:%S"), "pid": worker.pid} for worker in all_workers]
        return all_workers
    
    def stats(self):
        
        queue_data = {}
        workers = self.workers()
        queued = self.queued_jobs()

        with Connection(redis.from_url(self.url)):
            q = Queue()
            q.connection
            finished_job_registry = FinishedJobRegistry()
            started_jobs_registry = StartedJobRegistry()
            deferred_jobs_registry = DeferredJobRegistry()
            failed_jobs_registry = FailedJobRegistry()
            worker = Worker(['default'])
            
            queue_data['finished_jobs'] =  len(finished_job_registry)
            
            queue_data['started_jobs']  = len(started_jobs_registry)
            queue_data['deferred_jobs']  = len(deferred_jobs_registry)
            queue_data['failed_jobs']  = len(failed_jobs_registry)
            queue_data['workers']     = len(workers)
            queue_data['queued_jobs'] = len(queued)
            queue_data['active_jobs'] =  queue_data['started_jobs']+queue_data['queued_jobs']

        return queue_data