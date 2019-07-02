from django.core.management.base import BaseCommand, CommandError
from tasks.redisqueue import RedisQueue
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        rqueue = RedisQueue(settings.REDIS_URL)
        rqueue.worker()
        
