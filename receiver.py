from fastapi import FastAPI
from starlette.requests import Request

receiver_app = FastAPI()


@receiver_app.post("/")
async def post_handle(request: Request):
    print(request.headers.get('X-Celery-Id'))
    print(await request.body())
    return {"message": "OK"}
