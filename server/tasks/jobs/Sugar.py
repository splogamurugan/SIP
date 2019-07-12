from JobsAbstract import JobsAbstract
import redis
import time
class Sugar(JobsAbstract):
    '''
    A sugar CRM integration processor which accepts module and data(json_data) 
    which will be passed to the sugar CRM server through PUT/POST
    Please look into the HELP section about how to post the data

        Single Entry (Single data): 
        {'job_handler': 'Sugar.py', 'arguments': {'module': 'Opportunities', 'json_data': {'external_key': 'XX-AAAAA', 'account_id': 'XXXXXXX', 'id': 'XX-AAAAA'}}}

        Multi Entries (Multi data): 
        [{'job_handler': 'Sugar.py', 'arguments': {'module': 'Opportunities', 'json_data': {'external_key': 'XX-AAAAA', 'account_id': 'XXXXXXX', 'id': 'XX-AAAAA'}}},
        {'job_handler': 'Sugar.py', 'arguments': {'module': 'Opportunities', 'json_data': {'external_key': 'XX-AAAAA', 'account_id': 'XXXXXXX', 'id': 'XX-AAAAA'}}}]

    '''
    def generateOAuthToken(self):
        pass
    
    def request(self):
        pass
    
    def retry_count(self):
        return 0

    def handle(self, module:str, json_data:dict):
        time.sleep(2)
        print('its a dummy sugar')
        print(module, json_data)
        return True
    
