import librosa
import numpy as np

NOMBRE = "bpm"
COLUMNAS = ["bpm"]


def analizar(y, sr):
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    return {"bpm": round(float(np.atleast_1d(tempo)[0]), 1)}
