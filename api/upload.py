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

    subprocess.run([
        "demucs",
        save_path
    ])

    return {
        "status": "processed",
        "file": file.filename
    }