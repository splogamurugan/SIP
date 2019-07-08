from JobsAbstract import JobsAbstract

class Dummy(JobsAbstract):

    def retry_count(self):
        return 0

    def handle(self, **kwargs):
        print('its a dummy job to test')
        return True

