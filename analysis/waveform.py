import librosa
import numpy as np


class WaveformGenerator:

    def generate(self, audio_file):

        y, sr = librosa.load(audio_file)

        return y.tolist()[:5000]