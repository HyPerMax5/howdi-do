import numpy as np
import librosa
from multiprocessing import Process, Queue, Pipe


singer_extraction_finished:bool = False
song_extraction_finished:bool = False

singer_pitch_extraction_finished:bool = False
song_pitch_extraction_finished:bool = False


global rhythm_score
global pitch_score

MAX_SCORE:float = 100
MIN_SCORE:float = 0
FRAME_LENGTH:int = 2048
HOP_LENGTH:int = 512

karaoke_performance = './app/karaoke_performance.wav'
song_vocals = './app/JUDGEMENT-審判_(Vocals).wav'

performance_fmin = float(librosa.note_to_hz('C2'))
performance_fmax = float(librosa.note_to_hz('C7'))

song_fmin = float(librosa.note_to_hz('C2'))
song_fmax = float(librosa.note_to_hz('C7'))


#!Rhythm Extract
def extract_singer_rhythm(pipe):
	performance_y, performance_sr = librosa.load(karaoke_performance)
	print("Extracting performance rhythm...")
	tempo, beat_frames = librosa.beat.beat_track(y=performance_y, sr=performance_sr)
	singer_beat_frames = beat_frames
	#queue.put((1, singer_beat_frames))
	pipe.send(singer_beat_frames)
	pipe.close()
	singer_extraction_finished = True
	print("Singer rhythm done!");print("Singer extraction finished: ", singer_extraction_finished)
	return singer_extraction_finished

def extract_song_rhythm(pipe):
	song_y, song_sr = librosa.load(song_vocals)
	print("Extracting song rhythm...")
	tempo, beat_frames = librosa.beat.beat_track(y=song_y, sr=song_sr)
	song_beat_frames = beat_frames
	#queue.put((2, song_beat_frames))
	pipe.send(song_beat_frames)
	song_extraction_finished = True
	print("Song rhythm done!");print("Song extraction finished: ", song_extraction_finished)
	return song_extraction_finished
#//!Rhythm Extract



#!Pitch Extract
def extract_singer_pitch(pipe):
	performance_y, performance_sr = librosa.load(karaoke_performance)
	print("Starting performance pitch extraction")
	singer_pitch = librosa.yin(performance_y, fmin=performance_fmin, fmax=performance_fmax, 
 sr=performance_sr, frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)
	pipe.send(singer_pitch)
	singer_pitch_extraction_finished = True

	print("Finished singer pitch extraction!")
	return singer_pitch_extraction_finished

def extract_song_pitch(pipe):
	song_y, song_sr = librosa.load(song_vocals)
	print("Starting song pitch extraction.")
	song_pitch = librosa.yin(song_y, fmin=song_fmin, fmax=song_fmax, sr=song_sr,
 frame_length=FRAME_LENGTH, hop_length=HOP_LENGTH)
	pipe.send(song_pitch)
	song_pitch_extraction_finished = True

	print("Finished song pitch extraction!")
	return song_pitch_extraction_finished
	#//!Pitch Extract



#!Scoring
def score_rhythm(singer_beat_frames, song_beat_frames):
	global rhythm_score
	print("Scoring rhythm...!")
	rhythm_deviation = np.subtract(np.mean(np.abs(song_beat_frames)), np.mean(np.abs(singer_beat_frames)))
	rhythm_score = MAX_SCORE - (rhythm_deviation / 10)
	rhythm_score = max(min(rhythm_score, MAX_SCORE), MIN_SCORE)
	print("rhythm Deviation: ", rhythm_deviation)
	print("Rhythm Score:", rhythm_score)

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
		print("Mean squared error: ", mean_squared_error)
		print("Pitch Score: ", pitch_score)
#//!Scoring



if __name__=='__main__':
	

	pipe_parent, pipe_child = Pipe()
	pipe_parent1, pipe_child1 = Pipe()
	pipe_parent2, pipe_child2 = Pipe()
	pipe_parent3, pipe_child3 = Pipe()

	p1 = Process(target = extract_singer_rhythm, args=(pipe_child,))
	p1.start()


	p2 = Process(target = extract_song_rhythm, args=(pipe_child1,))
	p2.start()
	p1.join()
	p2.join()

	

	p3 = Process(target= extract_singer_pitch, args=(pipe_child2,))
	p3.start()
	p4 = Process(target= extract_song_pitch, args=(pipe_child3,))
	p4.start()
	p3.join()
	p4.join()

	while singer_extraction_finished == True and song_extraction_finished == True:
		print("Waiting on stuff....")
	else:
		score_rhythm(pipe_parent.recv(), pipe_parent1.recv())
		print("I gave you all I had... I did.")

		

	
	while singer_pitch_extraction_finished == False and song_pitch_extraction_finished == False:
		print("Help, I'm a cat and someone trapped me in this guy's code!!!")
#!		/\_/\ 
#!	( o.o ) 
#!	> ^ < 
	else:
		score_pitch(pipe_parent2.recv(), pipe_parent3.recv())
		print("もう終わりだ。。。")