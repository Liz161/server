import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    config_files = os.getenv('KUBECONFIG', default='~/.kube/config')
