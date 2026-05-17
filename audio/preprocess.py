from pydub import AudioSegment


def normalize_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    normalized = audio.normalize()
    normalized.export(file_path, format="wav")