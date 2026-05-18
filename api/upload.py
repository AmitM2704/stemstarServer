import os

from fastapi import APIRouter, UploadFile, File
from celery.result import AsyncResult

from workers.tasks import separate_song, celery

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...)
):

    save_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(save_path, "wb") as f:
        f.write(await file.read())

    # Queue Celery task instead of running Demucs directly
    job = separate_song.delay(save_path)

    return {
        "status": "queued",
        "task_id": job.id,
        "file": file.filename
    }


@router.get("/task/{task_id}")
def get_task(task_id: str):

    task = AsyncResult(task_id, app=celery)

    return {
        "task_id": task.id,
        "status": task.status,
        "result": task.result
    }