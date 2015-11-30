FFMPEG python wrapper
--------------------

A simple ffmpeg wrapper to convert Audio to mp3 or ogg whenever a new file is added to the watched directory.


Documentation for installation :

1) FFMPEG installation:
	
	sudo add-apt-repository ppa:kirillshkrogalev/ffmpeg-next
	sudo apt-get update
	sudo apt-get install ffmpeg


To convert existing files:

1) Change the value of "dir_to_watch" from "settings.json"

2) Run the script to convert audio within the root dir


		python convert_existing.py


To start a watch process:

1) Run the following to start the watch process


		python converter.py
