# request - asy way to convert Flask request form and args to route parameters
from flask import request
from app import app
from app import metrics
from kubernetes import client
import logging

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
v1 = client.CoreV1Api() # namespaces, services
v2 = client.AppsV1Api() #deployments

############################################
@app.route('/', methods=['GET'])
def hello_world():
    try:
        logger.info('Empty request')
        print('no requests') 
        return ('no requests')   
    except Exception as error:
        logger.error("Oh no! an error has been occurred, the error is: " + str(error))

############################################
# list of namespaces in the cluster
@app.route('/namespaces', methods=['GET'])
def namespaces():
    try:
        logger.info('Get: list of namespaces')
        nameSpaceList = v1.list_namespace()
        for nameSpace in nameSpaceList.items:
            print(nameSpace.metadata.name)
    except Exception as error:
        logger.error("Oh no! an error has been occurred, the error is: " + str(error))

############################################
# list of services in related namespace
@app.route('/services-<namespace>', methods=['GET'])
def services(namespace):
    try:
        logger.info('Get: list of services for namespace-%s',namespace)
        servicesList = v1.list_namespaced_service(namespace)
        for service in servicesList.items:
            print(service.metadata.name)    
    except Exception as error:
        logger.error("Oh no! an error has been occurred, the error is: " + str(error))

############################################
# list of deployments in related namespace
@app.route('/deployments-<namespace>', methods=['GET'])
def deployments(namespace):
    try:
        logger.info('Get: deployments for namespace-%s',namespace )
        deploymentsList = v2.list_namespaced_deployment(namespace)
        for deployment in deploymentsList.items:
            print(deployment.metadata.name)
        return
    except Exception as error:
        logger.error("Oh no! an error has been occurred, the error is: " + str(error))

############################################

@app.route('/pods-<deployment>', methods=['GET'])
def pods(deployment):
    try:
        logger.info('Get: pods for deployment-%s', deployment )        
        podsList = v1.list_pod_for_all_namespaces()
        deploymentsList = v2.list_deployment_for_all_namespaces()
        for pod in podsList.items:
            for deployment in deploymentsList.items:                
                if pod.metadata.labels.app.kubernetes.io/instance == deployment.spec.selector.matchLabels.app.kubernetes.io/instance and pod.metadata.labels.app.kubernetes.io/name == deployment.spec.selector.matchLabels.app.kubernetes.io/name :
                    print(pod.metadata.name)
    except Exception as error:
        logger.error("Oh no! somthing went worng with the posts page, the error is: " + str(error))

############################################

metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)