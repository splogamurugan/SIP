from JobsAbstract import JobsAbstract
import redis

class Sugar(JobsAbstract):

    def generateOAuthToken(self):
        pass
    
    def request(self):
        pass
    
    def retry_count(self):
        return 0

    def handle(self, module:str, json_data:dict):
        print(module, json_data)
        return True
