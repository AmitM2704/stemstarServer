import os

from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Body

from fastapi.responses import FileResponse

from celery.result import AsyncResult

from workers.tasks import (
    celery,
    separate_song
)

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


@router.post("/login")
async def login(data: dict = Body(...)):

    email = data.get("email")
    password = data.get("password")

    if (
        email == "admin@test.com"
        and
        password == "1234"
    ):

        return {
            "access_token": "fake_token"
        }

    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )


@router.get("/")
def home():

    return {
        "message": "API working"
    }


# Upload endpoint
@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...)
):

    save_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    # Save uploaded file
    with open(save_path, "wb") as f:

        f.write(
            await file.read()
        )

    # Queue Celery task
    job = separate_song.delay(save_path)

    return {
        "status": "queued",
        "task_id": job.id,
        "filename": file.filename
    }


# Check task status
@router.get("/task/{task_id}")
def get_task(task_id: str):

    task = AsyncResult(
        task_id,
        app=celery
    )

    return {
        "id": task.id,
        "status": task.status,
        "result": task.result,
    }


# Serve stem files
@router.get(
    "/stems/{song}/{stem_name}"
)
async def get_stem(
    song: str,
    stem_name: str
):

    file_path = os.path.join(
        "separated",
        "mdx_extra_q",
        song,
        stem_name
    )

    return FileResponse(file_path)