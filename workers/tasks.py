from celery import Celery

from app.models.ensemble import EnsembleSeparator


celery = Celery(
    "tasks",
    broker="redis://localhost:6379/0"
)


@celery.task

def separate_song(file_path):

    separator = EnsembleSeparator()

    separator.process(file_path)