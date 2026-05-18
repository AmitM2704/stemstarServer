import os
from celery import Celery

from models.ensemble import EnsembleSeparator

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

celery = Celery(
    "stemstar_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

separator = EnsembleSeparator()


@celery.task(bind=True)
def separate_song(self, file_path):

    try:
        result = separator.process(file_path)

        return {
            "status": "completed",
            "result": result,
        }

    except Exception as e:

        return {
            "status": "failed",
            "error": str(e),
        }