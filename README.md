# Job Processing Platform (django + django_restframework + redis + redis queue + reactjs + docker)
This provisions a platform to add any custom jobs and scale workers to process them. I have initially designed this to integrate sugarCRM application with any other enterprise application. However, this came up as a platform to add any job handler. It can be a Image processor, Video Processor, API caller, Scrapper, REST API call, or anything else.. 

It requires you to Add a job into the folder SIP/server/tasks/jobs/ and the job will be exposed to the API along with the required parameter list. Making a POST request to the API will ensure the job gets enqued and will be called with the supplied params. 


## The platform architecture
<img width="804" alt="image" src="https://user-images.githubusercontent.com/3910580/61511387-382c3580-aa14-11e9-9e33-9e65cb964c64.png">

## To Install
```sh
git clone git@github.com:splogamurugan/SIP.git
cd SIP
docker-compose build
docker-compose up -d
```
## To access the dashboard
Go to http://localhost:3000



## To scale up the workers
```sh
docker-compose up -d --scale worker=5
-- You can give the number based on your requirement
```

## To post a job
```sh
curl 'http://localhost:8000/bulk' -H 'Referer: http://localhost:3000/' -H 'Origin: http://localhost:3000' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36' -H 'Content-Type: multipart/form-data; boundary=----WebKitFormBoundary5YV1vElELRLRP5sk' --data-binary $'------WebKitFormBoundary5YV1vElELRLRP5sk\r\nContent-Disposition: form-data; name="job"\r\n\r\nImageProcessor.py\r\n------WebKitFormBoundary5YV1vElELRLRP5sk\r\nContent-Disposition: form-data; name="arguments"\r\n\r\n{"image_path":"/var/www/html/image.png", \n"output_path":"/var/export"}\r\n------WebKitFormBoundary5YV1vElELRLRP5sk--\r\n' --compressed


```

## Inbuilt SUGAR API Handler
This project comes along with a inbuilt SUGARCRM API Handler. 
### How it varies from other sugar api handlers?
Sugar API call needs Oauth-token to be passed on header. Before making any call the Oauth-token should be generated using a valid username and password. When more than one asyncronous API call generates the token old token gets expired. This API handler comes with a solution to handle that. It uses Redis as a token storage. All the API calls share the token instead of generating a new one. It automatically refreshes the token on token expiry. With this structure, N number of API calls can be made with help of workers (see the pic) without failure. 
### How to configure it?
* Open SIP/server/tasks/jobs/Sugar.py
* Look for method
```python
def handle(self, module:str, json_data:dict):
```
* There change the SugarAPI call like below 
```python
       s = SugarAPI(
            'https://localhost.sugarondemand.com', 
            'admin', 
            'asdf',
            'redis://sip_redis:6379/0'
        )
```
* The credentials may vary based on your need. 

### How to test it?
* Open http://localhost:3000/
* Choose "Sugar" at Job Name
* Paste the below JSON there
```json
{"module": "Tasks", "json_data": {"name": "XXXXX"}}
```
* It looks like this.. 
<img width="346" alt="image" src="https://user-images.githubusercontent.com/3910580/61527899-1f834600-aa3b-11e9-8686-44730736b213.png">
* Once posted you can see the job added to queue
<img width="1080" alt="image" src="https://user-images.githubusercontent.com/3910580/61528090-8dc80880-aa3b-11e9-99f7-6026864ea526.png">
* If everything goes good then it will create a task in your Sugar instance. 
* You can find the job in your finished list
<img width="1076" alt="image" src="https://user-images.githubusercontent.com/3910580/61528198-cc5dc300-aa3b-11e9-8fac-f4487b9a7d6c.png">




## To add a custom job handler (Your own functionality)
Please look into the a job handler SIP/server/tasks/jobs/ImageProcessor.py
```steps
CP SIP/server/tasks/jobs/ImageProcessor.py SIP/server/tasks/jobs/YourProcessor.py
Open SIP/server/tasks/jobs/YourProcessor.py
Change the python class as YourProcessor
```
Thats it.. It will be automatically exposed to API. You can check if its exposed to the API with the below command
```sh
curl 'http://localhost:8000/handlers' -H 'Accept: application/json' -H 'Referer: http://localhost:3000/' -H 'Origin: http://localhost:3000' -H 'Content-Type: application/json' --compressed
```sh
