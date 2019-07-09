from JobsAbstract import JobsAbstract
import time
class ImageProcessor(JobsAbstract):

    def retry_count(self):
        return 0

    def handle(self, image_path:str, output_path:str):
        time.sleep(2)
        print('its a image processing job to test')
        return True

