from django.core.management.base import BaseCommand, CommandError
from tasks.redisqueue import RedisQueue
from django.conf import settings

class Command(BaseCommand):
    help = 'Helper to handle the redis queue'
    
    def add_arguments(self, parser):
        parser.add_argument('opr', type=str)
        parser.add_argument('arg', type=str)

    def handle(self, *args, **options):
        #self.stdout.write('Helper to run the redis')
        arg = options['arg']
        opr = options['opr']
        rqueue = RedisQueue(settings.REDIS_URL)
        res =  getattr(rqueue, opr)(arg)
        self.stdout.write(str(res))