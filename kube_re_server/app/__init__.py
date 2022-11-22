from kubernetes import config
from flask import Flask
from config import Config
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

try:
# if requested from outside the cluster
    config.load_kube_config(Config.config_files)
except:
    config.load_incluster_config()

metrics = PrometheusMetrics(app)
# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

app.config.from_object(Config)

from app import routes


if __name__ == '__main__':
   app.run()