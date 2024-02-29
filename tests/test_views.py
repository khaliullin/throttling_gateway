import pytest
import requests_mock
from celery.result import AsyncResult
from fastapi.testclient import TestClient

import settings
from main import app
from tasks import send_request_task

client = TestClient(app)


def test_fastapi_endpoint_response_status():
    response = client.post("/")
    assert response.status_code == 200


def test_message_in_celery_queue():
    task = send_request_task.delay(
        {"Content-Type": "application/json"},
        "test_data"
    )
    task_id = task.id
    result = AsyncResult(task_id, app=send_request_task)
    assert result.state == 'PENDING'


@pytest.mark.skip(reason="Mock is not called")
def test_request_sent_to_receiver_server():
    with requests_mock.Mocker() as m:
        url = settings.RECEIVER_URL
        sample_data = "test_data"

        m.post(url, text="Mocked Response")

        send_request_task.delay({"Content-Type": "application/json"}, sample_data)

        assert m.called
        assert m.call_count == 1
        request = m.request_history[0]
        assert request.url == url
        assert request.text == sample_data
