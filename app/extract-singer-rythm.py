import numpy as np
import librosa

audio = './app/karaoke_performance.wav'

audio_y, audio_sr = librosa.load(ref)
tempo, beat_frames = librosa.beat.beat_track(y=audio_y, sr=audio_sr)
