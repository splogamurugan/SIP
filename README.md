# Job Processing Platform (django + django_restframework + redis + redis queue + reactjs + docker)
This is the platform I have designed to integrate the applications and to keep the applications heavy processes away from the applications. This I have initially designed to integrate sugarCRM application with anyother enterprise application. However, this came up as a platform to add any job handler. It can be a Image processor, Video Processor, API caller, Scrapper, anything else.. It requires you to Add a job into the folder SIP/server/tasks/jobs/ and the job will be exposed to the API. Later you can call the API


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

## To add a custom job
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
