import hashlib

import redis
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

import settings
from tasks import send_request_task

app = FastAPI()
redis_cli = redis.Redis().from_url(settings.REDIS_URL)


async def hash_request(request: Request) -> str:
    """
    Creates hash for request by headers, query params and body.
    """
    request_data = tuple([
        request.headers.get('cookie'),
        *request.query_params.items(),
        await request.body()
    ])
    tuple_bytes = str(request_data).encode()
    return hashlib.sha256(tuple_bytes).hexdigest()


async def duplicate_request(request: Request) -> bool:
    """
    Checks that request was processed within specified lifetime.
    """
    request_hash = await hash_request(request)
    if redis_cli.setnx(request_hash, b''):
        redis_cli.expire(request_hash, settings.DEDUPLICATION_TTL)
        return False
    return True


@app.get("/")
async def get_handle(request: Request):
    print(request.client)
    return {"message": "POST method required"}


@app.post("/")
async def post_handle(request: Request):
    if await duplicate_request(request):
        return Response(status_code=200)

    try:
        task = send_request_task.delay(dict(request.headers), await request.body())
    except Exception as e:
        # response is required in case of error, this is bad
        return Response(status_code=200)

    return JSONResponse(
        content={},
        status_code=200,
        headers={'X-Celery-Id': task.id},
    )
