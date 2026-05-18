import os
import subprocess
import time

from fastapi import HTTPException


from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Body
from fastapi import WebSocket

from fastapi.responses import FileResponse


router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# Store uploaded files temporarily
uploaded_files = {}


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
        "message":
        "API working"
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

    # Store file path
    uploaded_files[
        file.filename
    ] = save_path

    return {
        "status": "uploaded",
        "filename": file.filename
    }


# WebSocket for realtime progress
@router.websocket("/ws/progress")
async def websocket_progress(
    websocket: WebSocket
):

    await websocket.accept()

    print("WebSocket connected")

    try:

        while True:

            # Receive filename
            filename = await websocket.receive_text()

            print("Received:", filename)

            save_path = uploaded_files.get(
                filename
            )

            if not save_path:

                await websocket.send_text(
                    "FILE_NOT_FOUND"
                )

                continue

            print(
                "Starting Demucs..."
            )

            # Start Demucs
            process = subprocess.Popen(
                [
                    "demucs",
                    "--device",
                    "cpu",
                    "--two-stems",
                    "vocals",
                    save_path
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            # Stream realtime logs
            while True:

                output = process.stdout.readline()

                if (
                    output == ""
                    and
                    process.poll() is not None
                ):
                    break

                if output:

                    line = output.strip()

                    print(line)

                    await websocket.send_text(
                        line
                    )
            process.wait()
            print(
                "Demucs complete"
            )
            time.sleep(1)

            # Song name
            song_name = os.path.splitext(
                filename
            )[0]

            # Stem directory
            stem_dir = os.path.join(
                "separated",
                "htdemucs",
                song_name
            )

            print(
                "Stem dir:",
                stem_dir
            )

            stems = []

            # Read generated stems
            if os.path.exists(stem_dir):

                for stem_file in os.listdir(stem_dir):

                    stems.append({

                        "name": stem_file,

                        "url":
                        f"https://stemstarserver-81vf.onrender.com//stems/{song_name}/{stem_file}"
                    })

            # Send final websocket JSON
            await websocket.send_json({

                "type": "complete",

                "stems": stems
            })

    except Exception as e:

        print(
            "WebSocket Error:",
            e
        )

    finally:

        print(
            "WebSocket disconnected"
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
        "htdemucs",
        song,
        stem_name
    )

    return FileResponse(file_path)