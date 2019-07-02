import redis
from rq import Queue, Connection, Worker
from . import processor

class RedisQueue():
    conn = None

    def __init__(self, url:str):
        self.url = url

    def enqueue(self, content:str):
        with Connection(redis.from_url(self.url)):
            q = Queue()
            kwargs = {
              'content': content,
            }
            task = q.enqueue(processor.processor, kwargs=kwargs)
        return {
            'status': 'success',
            'data': {
                'id': task.get_id(),
                'status': task.get_status(),
                'result': task.result,
            }
        }
    
    def retrieve(self, task_id):
        with Connection(redis.from_url(self.url)):
            q = Queue()
            task = q.fetch_job(task_id)
        
        if task:
            return {
                'status': 'success',
                'data': {
                    'id': task.get_id(),
                    'status': task.get_status(),
                    'result': task.result,
                    'arguments': task.kwargs
                }
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
        
    def list(self):
        with Connection(redis.from_url(self.url)):
            q = Queue()
            return q.all()
    
        