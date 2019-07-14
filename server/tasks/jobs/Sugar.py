from JobsAbstract import JobsAbstract
import redis
import time

import sys
from os.path import abspath
from os.path import dirname
sys.path.append(dirname(abspath(__file__)))

from SugarAPI import SugarAPI

class Sugar(JobsAbstract):
    '''
    A sugar CRM integration processor which accepts module and data(json_data) 
    which will be passed to the sugar CRM server through PUT/POST
    Please look into the HELP section about how to post the data

        Single Entry (Single data): 
        {"module": "Tasks", "json_data": {"name": "XXXXX"}}

        Multi Entries (Multi data): 
        [{"module": "Tasks", "json_data": {"name": "YYYYYY"}},
        {"module": "Tasks", "json_data": {"name": "ZZZZZZ"}}]

    '''
    def generateOAuthToken(self):
        pass
    
    def request(self):
        pass
    
    def retry_count(self):
        return 0

    def handle(self, module:str, json_data:dict):
        #time.sleep(2)
        #print('its a dummy sugar')
        #print(module, json_data)
        s = SugarAPI(
            'https://X-int01.sugarondemand.com', 
            'U', 
            'P',
            'redis://sip_redis:6379/0'
        )
        #return s.upsert(module.capitalize(), json_data)

        time.sleep(2)
        return 'A Fake Execution Result'

        #return s.upsert(module.capitalize(), json_data)
    
