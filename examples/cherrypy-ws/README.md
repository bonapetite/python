RESTful Web Service using CherryPy
===================

Cherrypy is a light-weight Python framework for building web applications.  This project is a working example of a RESTful Web Service.  This implementation supports enabling SSL and/or basic authentication through the python command when starting the web service.  Enjoy!


Requirements
-------------
- Python 3 installed
- Cherrypy installed (For example using pip - *pip install cherrypy==13.1.0*)


Install and Run
-------------
- Download this directory by using the download link or clone the entire python project

- Navigate to cherrypy-ws directory
```
cd cherrypy-ws
```
- Run web service
```
python ws.py
```
- You can now check the web service is up and running by going to this url in the browser:
```
http://localhost?name=John

Welcome John, your GET request is successful
```
- You can test the POST request (e.g. in Postman) by using the same URL
```
http://localhost?name=John

Welcome John, your POST request is successful

```
Enable SSL
-------------
- Update **ws.config** with the correct paths to the certificate and private key files
```
[APP]
...
ssl.cert=<PATH_TO_CERT>
ssl.cert=<PATH_TO_PRIVATE_KEY>
...
```

- Run web service with ssl enabled
```
python ws.py --ssl
```

- You can now check the web service accepts https request by changing the protocol to https in the URL:
```
https://localhost?name=John

Welcome John, your GET request is successful
```

Enable Basic HTTP Authentication
-------------
- Update **ws.config** with the username and password:
```
[APP]
...
username=<YOUR_USERNAME>
password=<YOUR_PASSWORD>
...
```

- Run web service with basic authentication enabled
```
python ws.py --basicAuthentication
```

- Navigate to this URL in the browser and a prompt requesting for your credentials.  Enter the username and password that matches what are stored in the config file (from step 1), then you will be granted access and receive a success message.
```
https://localhost?name=John

Welcome John, your GET request is successful
```

> **Note:**
> You can enable both SSL and Basic Authentication as follows:
>  python ws.python --ssl --basicAuthentication

Docker
-------------
This is a good starting point if you want a light-weight Web Service running inside a docker container.  All you need is a Dockerfile to setup your environment and map the container port 80 or 443 to a host port for the web service to be accessible.