# request - asy way to convert Flask request form and args to route parameters
from flask import request
from prometheus_flask_exporter import PrometheusMetrics
from kubernetes import client , config
import logging
from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True

try:
# if requested from outside the cluster
    config.load_kube_config()
except:
    config.load_incluster_config()

metrics = PrometheusMetrics(app)
# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')


############################################

# create logger
logger = logging.getLogger('__name__')
level = logging.INFO
logger.setLevel(level)

# create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(level)

# add ch to logger
logger.addHandler(console_handler)

############################################
# setting of the cluster enviroment 
CoreV1Api = client.CoreV1Api() # namespaces, services, pods
AppsV1Api = client.AppsV1Api() #deployments

############################################
# welcome page with explanations.
@app.route('/', methods=['GET'])
def hello_world():
    try:
        logger.info('Empty request')
        toreturn = 'no requests \n\
to get all the namespaces in the cluster please refer to /namespaces \n\
to get all the services in some namespaces please refer to /services_<namespace> \n\
to get all the deployments in some namespaces please refer to /deployments_<namespace> \n\
to get all the pods in some deployment please refer to /pods_<deployment>\n\
to get metrics of this server refer to /metrics'
        print (toreturn)
        toreturn = 'no requests <br>\
to get all the namespaces in the cluster please refer to /namespaces <br>\
to get all the services in some namespaces please refer to /services_namespace <br>\
to get all the deployments in some namespaces please refer to /deployments_namespace <br>\
to get all the pods in some deployment please refer to /pods_deployment' 
        return (toreturn)   
    except Exception as error:
        logger.error("Oh no! an error has been occurred, the error is: " + str(error))

############################################
# list of namespaces in the cluster
@app.route('/namespaces')
def namespaces():
    try:
        logger.info('Get: list of namespaces')
        nameSpaceList = CoreV1Api.list_namespace()
        nameSpaceListt = ""
        for nameSpace in nameSpaceList.items:
            print(nameSpace.metadata.name)
            nameSpaceListt += nameSpace.metadata.name + "<br>"
        return ("list of namespaces:<br>" + nameSpaceListt)
    except Exception as error:
        logger.error("Oh no! an error has been occurred, the error is: " + str(error))
        return ("error", 404 )
############################################
# list of services in related namespace
@app.route('/services_<namespace>', methods=['GET'])
def services(namespace):
    try:
        logger.info('Get: list of services for namespace-%s',namespace)
        servicesList = CoreV1Api.list_namespaced_service(namespace)
        servicesListt = ""
        for service in servicesList.items:
            print(service.metadata.name)
            servicesListt += service.metadata.name + "<br>" 
        return ("list of services for namespace-" + namespace + " are:<br>"+ servicesListt)   
    except Exception as error:
        logger.error("Oh no! an error has been occurred, the error is: " + str(error))

############################################
# list of deployments in related namespace
@app.route('/deployments_<namespace>', methods=['GET'])
def deployments(namespace):
    try:
        logger.info('Get: deployments for namespace-%s',namespace )
        deploymentsList = AppsV1Api.list_namespaced_deployment(namespace)
        deploymentsListt = ""
        for deployment in deploymentsList.items:
            print(deployment.metadata.name)
            deploymentsListt += deployment.metadata.name + "<br>" 
        return ("list of deployments for namespace-" + namespace + " are:<br>"+ deploymentsListt)
    except Exception as error:
        logger.error("Oh no! an error has been occurred, the error is: " + str(error))

############################################
# list of pod on a specific deployment
@app.route('/pods_<deployment>', methods=['GET'])
def pods(deployment):
    try:
        logger.info('Get: pods for deployment-%s', deployment )        
        podsList = CoreV1Api.list_pod_for_all_namespaces()
        deploymentsList = AppsV1Api.list_deployment_for_all_namespaces()
        for deployments in deploymentsList.items:
            if deployments.metadata.name == deployment:
                label = deployments.spec.selector._match_labels
                deployments_match_labels = set(label.keys())
        podsListt = ""
        for pod in podsList.items:
            pod_labels = set(pod.metadata.labels.keys())               
            shared_keys = (deployments_match_labels).intersection(pod_labels)
            same = set(o for o in shared_keys if label[o] == pod.metadata.labels[o])
            if shared_keys == same and len(shared_keys)>0 :
                print(pod.metadata.name)
                podsListt += pod.metadata.name + "<br>" 
        return ("list of pods for deployment-" + deployment + " are:<br>"+ podsListt)
    except Exception as error:
        logger.error("Oh no! an error has been occurred, the error is: " + str(error))

############################################
# matrics exporter
metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)


if __name__ == '__main__':
   app.run()