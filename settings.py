import os

from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

RATE_LIMIT = f'{os.getenv("RATE_LIMIT", 8)}/s'
DEDUPLICATION_TTL = int(os.getenv('DEDUPLICATION_TTL', 1)) * 60
RECEIVER_URL = os.getenv('RECEIVER_URL', 'https://chatbot.com/webhook')
