
# Flask web-server


Using Flask to build a Restful API Server for existing kubernetes resources form from inside of the cluster.

## Features

- The server serves all the namespaces in the cluster please refer to /namespaces 
- The server serves all the services in some namespaces please refer to /services_<namespace>
- The server servest all the deployments in some namespaces please refer to /deployments_<namespace>
- The server serves all the pods in some deployment please refer to /pods_<deployment>
- The server also serve matrics on /matrics


## Installation

Install with pip:

```bash
$ pip install -r requirements.txt
```

    
## Flask Application Structure

```bash
.
├── Dockerfile
├── kube_re_server
│   ├── app
│   │   └── routes.py
└── └── requirements.txt
```
2 directories, 3 files


## Usage/Examples

Flask Configuration

Example
```python
app = Flask(__name__)
app.config['DEBUG'] = True
Configuring From Files
```

Example Usage
```python
app = Flask(__name__ )
app.config.from_pyfile('config.Development.cfg')
cfg example
```


## Flask settings



| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `DEBUG` | `boolean` |  True/False |
| `TESTING` | `boolean` |  True/False |


## Running Tests

To run tests, run the following command
Run Flask
flask run 
In flask, Default port is 5000

#### Run with Docker

```docker
$ docker build -t web-server .

$ docker run -p 5000:5000 --name web-server web-server 
```

It`s required to insert the kube-config of the cluster to the running docker container.

In image building, the webapp folder will also add into the image and the app will automatically run
the server on http://localhost:5000/

Changelog
Version 1.0 : basic flask-example with Flask-Restplus, Flask-Tesintg
