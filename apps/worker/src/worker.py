import os

from celery import Celery


broker_url = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

celery_app = Celery("letrado_worker", broker=broker_url, backend=result_backend)


@celery_app.task
def ping() -> str:
    return "pong"
