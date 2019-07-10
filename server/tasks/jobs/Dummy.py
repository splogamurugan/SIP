from JobsAbstract import JobsAbstract
import time
class Dummy(JobsAbstract):
    '''
        A dummy job created for the demo purpose which accepts any data 
        and keeps the processor to wait for 2 seconds then returns True

        Sample Input - Single Entry {"any_input":"XXXX"}
        Sample Input - Multi Entry [{"any_input":"XXXX"}, {"any_input":"YYYY"}]
    '''
    def retry_count(self):
        return 0

    def handle(self, **kwargs):
        time.sleep(2)
        print('its a dummy job to test')
        return True
    
