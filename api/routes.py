import os

from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Body
from fastapi import BackgroundTasks

from models.ensemble import (
    EnsembleSeparator
)

from fastapi.responses import FileResponse

# from celery.result import AsyncResult

# from workers.tasks import (
#     celery,
#     separate_song
# )
jobs = {}
processing = False

router = APIRouter()
def process_job(
    task_id,
    file_path
):

    global processing

    processing = True

    try:

        separator = EnsembleSeparator()

        result = separator.process(
            file_path
        )

        jobs[task_id] = {
            "status": "completed",
            "result": result
        }

    except Exception as e:

        jobs[task_id] = {
            "status": "failed",
            "error": str(e)
        }

    processing = False

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
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):

    global processing

    if processing:

        raise HTTPException(
            429,
            "Server busy"
        )

    save_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(
        save_path,
        "wb"
    ) as f:

        while chunk := await file.read(
            1024 * 1024
        ):
            f.write(chunk)

    task_id = file.filename

    jobs[task_id] = {
        "status": "processing"
    }

    background_tasks.add_task(
        process_job,
        task_id,
        save_path
    )

    return {
        "task_id": task_id
    }
# Check task status
@router.get(
    "/task/{task_id}"
)
def get_task(
    task_id: str
):

    print(
        "jobs:",
        jobs.keys()
    )

    return jobs.get(
        task_id,
        {
            "status":"not_found"
        }
    )

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