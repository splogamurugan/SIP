from JobsAbstract import JobsAbstract
import time
class ImageProcessor(JobsAbstract):
    '''
        A dummy Image processor which supposed to convert 
        the image (image_path) into thumbnails.
        The thumbnails will be exported to the path: output_path

        Sample Input - Single (Copy paste the below JSON to the textarea and submit) 
        {"image_path":"/var/www/html/image.png", 
        "output_path":"/var/export"}

        Sample Input - Multiple (Copy paste the below JSON to the textarea and submit) 
        [{"image_path":"/var/www/html/image.png", 
        "output_path":"/var/export"},
        {"image_path":"/var/www/html/image2.png", 
        "output_path":"/var/export"}]

    '''
    def retry_count(self):
        return 0

    def handle(self, image_path:str, output_path:str):
        time.sleep(2)
        print('its a image processing job to test')
        return True

