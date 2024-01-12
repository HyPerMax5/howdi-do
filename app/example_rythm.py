import numpy as np
import librosa

"""
   Extracts rhythm, calculates deviation and gives a score based on that.

   Limitations:
   Audio has to be the same length as the reference audio for accurate scoring,
   I'd advise to use the observer pattern to begin your recording at the exact moment
   your song audio begins to play.
   """

max_score:float = 100
min_score:float = 0


#*Your audio to score.
audio = './app/karaoke_performance.wav'

#*The reference audio.
ref = './app/JUDGEMENT-審判_(Vocals).wav'

#*Loads the respective audio files
audio_y, audio_sr = librosa.load(audio)
ref_y, ref_sr = librosa.load(ref)

#*Extracts tempo and beat frames.
tempo, beat_frames = librosa.beat.beat_track(y=audio_y, sr=audio_sr)
ref_tempo, ref_beat_frames = librosa.beat.beat_track(y=ref_y, sr=ref_sr)
print(tempo); print(beat_frames)
print(ref_tempo); print(ref_beat_frames)

#*Subtracts the result arrays to get the difference.
rhythm_deviation = np.subtract(np.mean(np.abs(ref_beat_frames)), np.mean(np.abs(beat_frames)))
print("Rhythm Deviation:", rhythm_deviation)

#*Score is attained.
rhythm_score = max_score - (rhythm_deviation / 10)

#*Clamps the score to a minimum and maximum value, this is mainly to avoid negative digits if something goes wrong.
rhythm_score = max(min(rhythm_score, max_score), min_score)
print("Rhythm Score:", rhythm_score)