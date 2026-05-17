import os
import uuid


def generate_filename(filename):
    ext = filename.split(".")[-1]
    return f"{uuid.uuid4()}.{ext}"


def ensure_directory(path):
    os.makedirs(path, exist_ok=True)