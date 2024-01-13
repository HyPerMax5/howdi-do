from math import atan
import numpy as np
import librosa
import time

max_score:float = 100
min_score:float = 0


frame_length:int = 2048
""" Higher frame length increases pitch extraction accuracy at
the cost of processing speed. """

hop_length:int = 512
""" Decreasing hop length improves accuracy at the cost of processing time. """

#*Your audio to score.
audio = './app/karaoke_performance.wav'


#*The reference audio.
ref = './app/JUDGEMENT-審判_(Vocals).wav'


#*Loads the respective audio files
audio_y, audio_sr = librosa.load(audio)
ref_y, ref_sr = librosa.load(ref)


#*Note range converted to hz for your audio.
#*If this is no pre declared as a float, it refuses to work!
audio_fmin = float(librosa.note_to_hz('C2'))
audio_fmax = float(librosa.note_to_hz('C7'))

ref_fmin = float(librosa.note_to_hz('C2'))
ref_fmax = float(librosa.note_to_hz('C7'))


#*Extracts pitch from your audio.
print("Starting audio pitch extraction")
start_time = time.time()

audio_pitch = librosa.yin(audio_y, fmin=audio_fmin, fmax=audio_fmax, 
 sr=audio_sr, frame_length=frame_length, hop_length=hop_length)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Finished audio pitch extraction in : {elapsed_time} seconds")


#*Extracts pitch from reference audio.
print("Starting reference audio pitch extraction.")
start_time = time.time()

ref_pitch = librosa.yin(ref_y, fmin=ref_fmin, fmax=ref_fmax, sr=ref_sr,
 frame_length=frame_length, hop_length=hop_length)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Finished reference audio pitch extraction in : {elapsed_time} seconds")


#*Increases array size to match, then calculates mean squared error.
#*....not like I actually know what mean squared error means.

if audio_pitch[0].size > ref_pitch[0].size:
   newarr = np.pad(audio_pitch, (0,len(audio_pitch)-len(ref_pitch)))
   ref_pitch = np.pad(ref_pitch, (0,len(audio_pitch)-len(ref_pitch)), mode='constant', constant_values=0)
   mean_squared_error = np.subtract((np.mean(newarr)), (np.mean(ref_pitch)))**2
elif audio_pitch[0].size < ref_pitch[0].size: 
   newarr = np.pad(audio_pitch, (0,len(ref_pitch)-len(audio_pitch)))
   audio_pitch = np.pad(audio_pitch, (0,len(ref_pitch)-len(audio_pitch)), mode='constant', constant_values=0)
   mean_squared_error = np.subtract((np.mean(ref_pitch)), (np.mean(newarr)))**2
else:
   mean_squared_error = np.subtract((np.mean(audio_pitch)), (np.mean(ref_pitch)))**2
   print("Mean squared error: ", mean_squared_error)



#*Score is attained.
pitch_score = max_score - (mean_squared_error / 1000)
print("Unclamped pitch score: ", pitch_score)

#*Clamps the score to a minimum and maximum value, this is mainly to avoid negative digits if something goes wrong.
pitch_score = max(min(pitch_score, max_score), min_score)

print("Pitch Score: ", pitch_score)