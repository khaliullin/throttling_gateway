import os

from celery import Celery

from settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    CELERY_BROKER_URL,
)
celery.conf.result_backend = os.environ.get(
    CELERY_RESULT_BACKEND,
)
celery.conf.include = ["tasks"]
