import requests

import settings
from worker import celery


@celery.task(name="send_request", rate_limit=settings.RATE_LIMIT)
def send_request_task(headers, body):
    headers['X-Celery-Id'] = send_request_task.request.id
    requests.post(
        url=settings.RECEIVER_URL,
        headers=headers,
        data=body,
    )
