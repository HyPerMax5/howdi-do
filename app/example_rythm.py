import numpy as np
import librosa

max_score:float = 100
min_score:float = 0

audio = './app/karaoke_performance.wav'
ref = './app/JUDGEMENT-審判_(Vocals).wav'

audio_y, audio_sr = librosa.load(ref)
ref_y, ref_sr = librosa.load(ref)

tempo, beat_frames = librosa.beat.beat_track(y=audio_y, sr=audio_sr)
ref_tempo, ref_beat_frames = librosa.beat.beat_track(y=ref_y, sr=ref_sr)




rhythm_deviation = np.subtract(np.mean(np.abs(ref_beat_frames)), np.mean(np.abs(beat_frames)))
print(rhythm_deviation)

#rhythm_deviation = np.mean(np.abs(beat_frames - ref_beat_frames))
rhythm_score = max_score - (rhythm_deviation / 10)
#rhythm_score = max(min(rhythm_score, max_score), min_score)
print("Rhythm Score:", rhythm_score)


