import numpy as np
import librosa
from multiprocessing import Process
from multiprocessing import Queue


#!This works now, Python just needs a lot more manual handling than GDScript ;)

global singer_extraction_finished
singer_extraction_finished:bool = False
global song_extraction_finished
song_extraction_finished:bool = False



global rhythm_score
rythm_score:float = 0


max_score:float = 100
min_score:float = 0

karaoke_performance = './app/karaoke_performance.wav'
song_vocals = './app/JUDGEMENT-審判_(Vocals).wav'


def extract_singer_rythm(queue):
	print("Loading performance...")
	karaoke_performance_y, karaoke_performance_sr = librosa.load(karaoke_performance)
	print("Extracting performance rythm...")
	tempo, beat_frames = librosa.beat.beat_track(y=karaoke_performance_y, sr=karaoke_performance_sr)
	singer_beat_frames = beat_frames
	queue.put((1, singer_beat_frames))
	singer_extraction_finished = True
	print("Singer rythm done!");print("Singer extraction finished: ", singer_extraction_finished)
	return singer_extraction_finished

def extract_song_rythm(queue):
	print("Loading song...")
	song_vocals_y, song_vocals_sr = librosa.load(song_vocals)
	print("Extracting song rythm...")
	tempo, beat_frames = librosa.beat.beat_track(y=song_vocals_y, sr=song_vocals_sr)
	song_beat_frames = beat_frames
	queue.put((2, song_beat_frames))
	song_extraction_finished = True
	print("Song rythm done!");print("Song extraction finished: ", song_extraction_finished)
	return song_extraction_finished

def score_rythm(singer_beat_frames, song_beat_frames):
	print("Scoring Rythm...!")
	rhythm_deviation = np.subtract(np.mean(np.abs(song_beat_frames)), np.mean(np.abs(singer_beat_frames)))
	rhythm_score = max_score - (rhythm_deviation / 10)
	rhythm_score = max(min(rhythm_score, max_score), min_score)
	print("Rythm Deviation: ", rhythm_deviation)
	print("Rhythm Score:", rhythm_score)
	return rhythm_score


if __name__=='__main__':

	queue = Queue()
	p1 = Process(target = extract_singer_rythm, args=(queue,))
	p1.start()
	p2 = Process(target = extract_song_rythm, args=(queue,))
	p2.start()
	p1.join()
	p2.join()
	result1 = queue.get()
	result2 = queue.get()


	while singer_extraction_finished == True and song_extraction_finished == True:
		print("Waiting....")
	else:
		score_rythm(result1[1], result2[1])
		print("Weeee, done!")
