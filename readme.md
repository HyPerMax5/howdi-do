# Howdi-do, a karaoke scoring system

I've always loved karaoke, however most things out there 
don't have a scoring system.  
To me the scoring makes things much more fun, 
without it, things such as being able to destroy your friends are impossible.  
How would one be able to set a high score if there are no scores?  

How do you even set ridiculously good high scores that your friends
 could never dream of beating if there is no score?

## Info
Howdi-do uses <a href = "https://github.com/librosa/librosa">librosa</a><sub><sup><sup>Copyright (c) 2013--2023, librosa development team</sup></sup></sub> to
extract and analyze beat data.  
Pitch scoring has been implemented.
  
The current implementation would require 2
files, one being a recording of your singing and the other being a vocals file
of the song you're singing.

This is intended to be used as a "scoring backend", standalone use is possible  
but it's designed to get its inputs from another script.

I'm building this to use in <a href = "https://github.com/HyPerMax5/RyuGaKaraoke">my karaoke system</a>.

## Usage
``pip install -r requirements.txt``  
Open ./app folder in your shell of choice.  
``python __main__.py "[path to karaoke recording]" "[Path to song vocals]"``

Results are printed to stdout, might re-implement save to file via another  
sys argument, however this is mainly intended to be used as a backend.  
And I have an irrational hatred for writing small files to disk instead of  
just keeping the variables in memory, especially when it's only 4 things.

