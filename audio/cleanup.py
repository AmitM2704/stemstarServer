from pydub import AudioSegment


def trim_silence(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    trimmed = audio.strip_silence()
    trimmed.export(output_file, format="wav")