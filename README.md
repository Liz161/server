Flask web-server
Using Flask to build a Restful API Server for existing kubernetes resources form from inside of the cluster.

The server serves all the namespaces in the cluster please refer to /namespaces 
The server serves all the services in some namespaces please refer to /services_<namespace>
The server servest all the deployments in some namespaces please refer to /deployments_<namespace>
The server serves all the pods in some deployment please refer to /pods_<deployment>
The server also serve matrics on /matrics

Installation
Install with pip:

$ pip install -r requirements.txt

Flask Application Structure
.
├── Dockerfile
├── kube_re_server
│   ├── app
│   │   └── routes.py
└── └── requirements.txt
2 directories, 3 files

Flask Configuration
Example
app = Flask(__name__)
app.config['DEBUG'] = True
Configuring From Files
Example Usage
app = Flask(__name__ )
app.config.from_pyfile('config.Development.cfg')
cfg example

##Flask settings
DEBUG = True  # True/False
TESTING = False

....

Run Flask
flask run 
In flask, Default port is 5000

Run with Docker
$ docker build -t web-server .

$ docker run -p 5000:5000 --name web-server web-server 

it is required to insert the kube config of the cluster to the runinig docker container.
In image building, the webapp folder will also add into the image and the app will automaticly will run
the server will be serve on http://localhost:5000/

Changelog
Version 1.0 : basic flask-example with Flask-Restplus, Flask-Tesintg