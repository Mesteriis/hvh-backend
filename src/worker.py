import os

import celery_tasks  # noqa: F401
from celery import Celery

from core.config import settings

celery = Celery(__name__)
celery.conf.broker_url = settings.celery_broker_url
celery.conf.result_backend = settings.celery_result_backend
