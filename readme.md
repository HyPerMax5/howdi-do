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
I intend to also implement pitch based scoring.
  
The current implementation would require 2
files, one being a recording of your singing and the other being a vocals file
of the song you're singing.

This is intended to be used as a "scoring backend", standalone use is possible  
but it's designed to get its inputs from another script.

I'm building this to use in my karaoke system <a href = "https://github.com/HyPerMax5/RyuGaKaraoke">Ryū Ga Karaoke</a>.


