from JobsAbstract import JobsAbstract
import time
class Dummy(JobsAbstract):

    def retry_count(self):
        return 0

    def handle(self, **kwargs):
        time.sleep(2)
        print('its a dummy job to test')
        return True

