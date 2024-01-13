import numpy as np
import librosa
import sys
from concurrent.futures import ThreadPoolExecutor


singer_extraction_finished:bool = False
song_extraction_finished:bool = False

singer_pitch_extraction_finished:bool = False
song_pitch_extraction_finished:bool = False

global rhythm_score
global tempo_score
global pitch_score
rhythm_score:float = 0
tempo_score:float = 0
pitch_score:float = 0

MAX_SCORE:float = 100
MIN_SCORE:float = 0
FRAME_LENGTH:int = 2048
HOP_LENGTH:int = 512

karaoke_performance = sys.argv[1]
song_vocals = sys.argv[2]

performance_fmin = float(librosa.note_to_hz('C2'))
performance_fmax = float(librosa.note_to_hz('C7'))

song_fmin = float(librosa.note_to_hz('C2'))
song_fmax = float(librosa.note_to_hz('C7'))


#!Rhythm Extract
def extract_singer_rhythm():
	performance_y, performance_sr = librosa.load(karaoke_performance)
	tempo, beat_frames = librosa.beat.beat_track(y=performance_y, sr=performance_sr)
	singer_tempo = tempo
	singer_beat_frames = beat_frames
	singer_extraction_finished = True
	return singer_beat_frames, singer_tempo, singer_extraction_finished

def extract_song_rhythm():
	song_y, song_sr = librosa.load(song_vocals)
	tempo, beat_frames = librosa.beat.beat_track(y=song_y, sr=song_sr)
	song_tempo = tempo
	song_beat_frames = beat_frames
	song_extraction_finished = True
	return song_beat_frames, song_tempo, song_extraction_finished
#//!Rhythm Extract


#!Pitch Extract
def extract_singer_pitch():
	performance_y, performance_sr = librosa.load(karaoke_performance)
	singer_pitch = librosa.yin(performance_y, fmin=performance_fmin, fmax=performance_fmax, 
 sr=performance_sr, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)
	singer_pitch_extraction_finished = True
	return singer_pitch, singer_pitch_extraction_finished

def extract_song_pitch():
	song_y, song_sr = librosa.load(song_vocals)
	song_pitch = librosa.yin(song_y, fmin=song_fmin, fmax=song_fmax, sr=song_sr,
 frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)
	song_pitch_extraction_finished = True
	return song_pitch, song_pitch_extraction_finished
	#//!Pitch Extract


#!Scoring
def score_rhythm(singer_beat_frames, song_beat_frames):
	global rhythm_score
	rhythm_deviation = np.subtract(np.mean(np.abs(song_beat_frames)), np.mean(np.abs(singer_beat_frames)))
	rhythm_score = MAX_SCORE - (rhythm_deviation / 10)
	rhythm_score = max(min(rhythm_score, MAX_SCORE), MIN_SCORE)
	print("Rhythm Score:", rhythm_score)
	return rhythm_score

def score_tempo(singer_tempo, song_tempo):
	global tempo_score
	tempo_deviation = np.subtract(song_tempo, singer_tempo)
	tempo_score = MAX_SCORE - (tempo_deviation)
	tempo_score = max(min(tempo_score, MAX_SCORE), MIN_SCORE)
	print("Tempo Score:", tempo_score)
	return tempo_score

def score_pitch(singer_pitch, song_pitch):
	global pitch_score
	if singer_pitch[0].size > song_pitch[0].size:
		newarr = np.pad(singer_pitch, (0,len(singer_pitch)-len(song_pitch)))
		song_pitch = np.pad(song_pitch, (0,len(singer_pitch)-len(song_pitch)), mode='constant', constant_values=0)
		mean_squared_error = np.subtract((np.mean(newarr)), (np.mean(song_pitch)))**2
	elif singer_pitch[0].size < song_pitch[0].size:
		newarr = np.pad(singer_pitch, (0,len(song_pitch)-len(singer_pitch)))
		singer_pitch = np.pad(singer_pitch, (0,len(song_pitch)-len(singer_pitch)), mode='constant', constant_values=0)
		mean_squared_error = np.subtract((np.mean(song_pitch)), (np.mean(newarr)))**2
	else:
		mean_squared_error = np.subtract((np.mean(singer_pitch)), (np.mean(song_pitch)))**2
		pitch_score = MAX_SCORE - (mean_squared_error / 1000)
		pitch_score = max(min(pitch_score, MAX_SCORE), MIN_SCORE)
		print("Pitch Score:", pitch_score)
		return pitch_score

def score(rhythm_score, tempo_score, pitch_score):
	score = (rhythm_score + tempo_score + pitch_score) / 3
	print("Song Score:", score)
	return score
#//!Scoring


with ThreadPoolExecutor(max_workers=4) as executor:
 worker1 = executor.submit(extract_singer_rhythm)
 worker2 = executor.submit(extract_song_rhythm)
 worker3 = executor.submit(extract_singer_pitch)
 worker4 = executor.submit(extract_song_pitch)

 singer_beat_frames, singer_tempo, singer_extraction_finished = worker1.result()
 song_beat_frames, song_tempo, song_extraction_finished = worker2.result()
 singer_pitch, singer_pitch_extraction_finished = worker3.result()
 song_pitch, song_pitch_extraction_finished = worker4.result()

while singer_extraction_finished == False and song_extraction_finished == False:
		pass 
	#//like I'm passin' on anything but gruelling manual labour because I was too dumb to get good grades all those years ago hah gottem :-(
else:
	score_rhythm(singer_beat_frames, song_beat_frames)
	score_tempo(singer_tempo, song_tempo)
	#*I gave you all I had... I did.

while singer_pitch_extraction_finished == False and song_pitch_extraction_finished == False:
	pass
	#?Help, I'm a cat and someone trapped me in this guy's code!!!
#!		/\_/\ 
#!	( o.o ) 
#!	> ^ < 
else:
	score_pitch(singer_pitch, song_pitch)

while singer_extraction_finished == False and song_extraction_finished == False and singer_pitch_extraction_finished == False and song_pitch_extraction_finished == False:
	pass
else:
	score(rhythm_score, tempo_score, pitch_score)
	#*おわりですニャー