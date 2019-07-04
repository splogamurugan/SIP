from django.core.management.base import BaseCommand, CommandError
from tasks.redisqueue import RedisQueue
from django.conf import settings

import json
from json.decoder import JSONDecodeError


class Command(BaseCommand):
    help = 'Helper to handle the redis queue'
    
    def add_arguments(self, parser):
        parser.add_argument('opr', type=str)
        parser.add_argument('arg', type=str, nargs='?', default='')

    def handle(self, *args, **options):
        #self.stdout.write('Helper to run the redis')
        arg = options.get('arg', '')

        opr = options.get('opr')
        rqueue = RedisQueue(settings.REDIS_URL)
        
        if (opr == 'enqueue'):
            try:
                arg = arg.replace("'", "\"")
                arg = json.loads(arg)
            except JSONDecodeError as e:
                print(e)
                return
        try:
            res =  getattr(rqueue, opr)(arg)
        except TypeError:
            res =  getattr(rqueue, opr)()

        self.stdout.write(str(res))